const expressionEl = document.querySelector('[data-expression]');
const displayEl = document.querySelector('[data-display]');
const buttons = document.querySelectorAll('button');

let currentExpression = '';

function updateDisplay() {
  expressionEl.textContent = currentExpression || '0';
}

function appendValue(value) {
  currentExpression += value;
  updateDisplay();
}

function clearExpression() {
  currentExpression = '';
  updateDisplay();
}

function backspace() {
  currentExpression = currentExpression.slice(0, -1);
  updateDisplay();
}

async function evaluateExpression() {
  const expression = currentExpression.trim();
  if (!expression) {
    displayEl.textContent = '0';
    return;
  }

  expressionEl.textContent = expression;
  displayEl.textContent = '…';

  try {
    const response = await fetch('/api/calc', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expression }),
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || 'Calculation failed');
    }

    displayEl.textContent = payload.result;
    currentExpression = payload.result.toString();
  } catch (error) {
    displayEl.textContent = error.message;
    currentExpression = '';
  }
}

buttons.forEach((button) => {
  button.addEventListener('click', () => {
    const action = button.dataset.action;
    const value = button.dataset.value;

    if (action === 'clear') {
      clearExpression();
      return;
    }

    if (action === 'backspace') {
      backspace();
      return;
    }

    if (action === 'equals') {
      evaluateExpression();
      return;
    }

    if (value !== undefined) {
      appendValue(value);
    }
  });
});

updateDisplay();
