const form = document.getElementById('metricsForm');
const resultContainer = document.getElementById('resultContainer');
const resSleepScore = document.getElementById('resSleepScore');
const resStressLevel = document.getElementById('resStressLevel');
const shapBtn = document.getElementById('shapBtn');
const shapImageContainer = document.getElementById('shapImageContainer');
const shapImage = document.getElementById('shapImage');

let currentPredictionId = null; 

form.addEventListener('submit', async (event) => {
    event.preventDefault(); 

    const formData = new FormData(form);
    const payload = {};

    formData.forEach((value, key) => {
        if (key === 'gender' || key === 'physical_activity_level' || key === 'diet_type') {
            payload[key] = value;
        } else {
            payload[key] = value.includes('.') ? parseFloat(value) : parseInt(value, 10);
        }
    });

    try {
        const response = await fetch('/api/v1/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('Ошибка при ответе бэкенда');
        }

        const data = await response.json();

        currentPredictionId = data.id;

        resSleepScore.textContent = data.sleep_quality_score;
        resStressLevel.textContent = data.daily_stress_level;

        resultContainer.style.display = 'block';
        shapImageContainer.style.display = 'none';

    } catch (error) {
        alert('Произошла ошибка: ' + error.message);
    }
});

shapBtn.addEventListener('click', () => {
    if (!currentPredictionId) return;

    shapImage.src = `/api/v1/predict/${currentPredictionId}/explanation`;
    
    shapImageContainer.style.display = 'block';
});


const toggleBmiCalc = document.getElementById('toggleBmiCalc');
const bmiCalcContainer = document.getElementById('bmiCalcContainer');
const calcHeight = document.getElementById('calcHeight');
const calcWeight = document.getElementById('calcWeight');
const bmiInput = document.getElementById('bmiInput');

toggleBmiCalc.addEventListener('click', (event) => {
    event.preventDefault(); 
    
    if (bmiCalcContainer.style.display === 'none') {
        bmiCalcContainer.style.display = 'block';
        toggleBmiCalc.textContent = 'Скрыть калькулятор ИМТ';
    } else {
        bmiCalcContainer.style.display = 'none';
        toggleBmiCalc.textContent = 'Не помню свой ИМТ (рассчитать по росту и весу)';
    }
});

function calculateBmi() {
    const heightCm = parseFloat(calcHeight.value);
    const weightKg = parseFloat(calcWeight.value);

    if (heightCm > 0 && weightKg > 0) {
        const heightMeters = heightCm / 100; 
        const bmi = weightKg / (heightMeters * heightMeters); 
        
        bmiInput.value = bmi.toFixed(1);
    }
}

calcHeight.addEventListener('input', calculateBmi);
calcWeight.addEventListener('input', calculateBmi);