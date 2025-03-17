import asyncio
import random
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")


import random
import asyncio

class MovieSensor:
    def __init__(self):
        self.current_value = 100  # Начальное значение
        self.values_list = []  # Список для хранения значений
        self.light_status = []

        self.is_running = False
        self.is_increasing = False  # Флаг для отслеживания направления изменения значения

    async def add_answer(self):
        self.is_running = True
        self.is_increasing = False  # Сначала уменьшение значения
        while True:
            if not self.is_running:
                break
            
            # Добавляем текущее значение в список значений
            self.add_value(self.current_value)

            # Проверяем текущее значение и обновляем статус освещения
            if self.current_value < 50:
                self.light_status.append("Освещение включено")
            else:
                self.light_status.append("Освещение выключено")

            # Изменяем значение в зависимости от флага
            if self.is_increasing:
                # Увеличиваем значение на 10, если оно меньше 100
                if self.current_value < 90:
                    self.current_value += random.randint(5, 10)
                else:
                    # Если значение достигло 100, начинаем уменьшать его
                    self.is_increasing = False
            else:
                # Уменьшаем значение на 10, если оно больше 0
                if self.current_value > 15:
                    self.current_value -= random.randint(5, 10)
                else:
                    # Если значение достигло 0, начинаем увеличивать его
                    self.is_increasing = True

            await asyncio.sleep(1)  # Асинхронная пауза

    def add_value(self, value):
        self.values_list.append(value)  # Обновляем список значений

    def stop_answer(self):
        breakdown = random.randint(1, 3)
        match breakdown:
            case 1:
                self.values_list.append("No signal")
                self.light_status.append("Неисправность на датчике движения. Работа остановлена")
                self.is_running = False
            case 2:
                self.values_list.append("No signal")
                self.light_status.append("Поломка в системе управления. Работа остановлена")
                self.is_running = False
            case 3:
                self.values_list.append("No signal")
                self.light_status.append("Поломка в реле освещения. Работа остановлена")
                self.is_running = False


# Создаем экземпляр MovieSensor без фоновой задачи на старте.
sensor = MovieSensor()


# Функция для запуска в фоне.
def run_add_answer(sensor):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(sensor.add_answer())


@app.get("/start-task")
async def start_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_add_answer, sensor)


@app.get("/light-status")
async def get_light_status():
    return {"light_status": sensor.light_status}


@app.get("/stop-task")
async def stop_task():
    sensor.stop_answer()
    return {"message": "Работа остановлена"}


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/values")
async def get_values():
    return JSONResponse(content={"values": sensor.values_list})


# Запуск приложения (без фоновой задачи на старте).
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

