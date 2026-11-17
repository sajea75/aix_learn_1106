import os
import io
import base64
import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.conf import settings
from django.shortcuts import render

# 1. 최상위 폴더(BASE_DIR)에서 모델과 스케일러 불러오기
MODEL_PATH = os.path.join(settings.BASE_DIR, 'fish_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'fish_scaler.pkl')

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

# 모델에 저장된 클래스 목록 가져오기 (없을 경우 기본 리스트 사용)
FISH_CLASSES = list(getattr(model, 'classes_', [
    'Bream', 'Parkki', 'Perch', 'Pike', 'Roach', 'Smelt', 'Whitefish'
]))


def index(request):
    context = {}

    if request.method == 'POST':
        # 2. HTML 폼에서 입력받은 5개 특성 가져오기
        weight = float(request.POST.get('weight'))
        length = float(request.POST.get('length'))
        diagonal = float(request.POST.get('diagonal'))
        height = float(request.POST.get('height'))
        width = float(request.POST.get('width'))

        # 2차원 배열로 변환 후 StandardScaler로 스케일링 적용
        input_data = np.array([[weight, length, diagonal, height, width]])
        input_scaled = scaler.transform(input_data)

        # 3. 스케일링된 데이터로 생선 품종 및 확률 예측
        pred_fish = model.predict(input_scaled)[0]
        proba = model.predict_proba(input_scaled)[0]
        max_proba = round(float(np.max(proba)), 3)
        proba_rounded = np.round(proba, 3)

        # 4. 전체 확률 막대 그래프 생성
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.bar(FISH_CLASSES, proba, color='#4A90E2')
        ax.set_ylim(0, 1.1)
        ax.set_ylabel('Probability')
        ax.set_title('Fish Species Prediction Probability')

        for bar, p in zip(bars, proba_rounded):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f'{p:.3f}', ha='center', va='bottom', fontsize=9)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close(fig)
        graph_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        # 5. 결과 데이터를 index.html로 전달
        context = {
            'weight': weight,
            'length': length,
            'diagonal': diagonal,
            'height': height,
            'width': width,
            'pred_fish': pred_fish,
            'max_proba': f'{max_proba:.3f}',
            'classes_str': str(FISH_CLASSES),
            'proba_str': str(proba_rounded),
            'graph': graph_base64,
        }

    return render(request, 'home/index.html', context)