from abc import ABC, abstractmethod
from datetime import date
from threading import Lock


class Place(ABC):  # Абстрактный класс места проведения
    def __init__(self, place_title: str):
        self.place_title = place_title

    @abstractmethod
    def __str__(self):
        pass


class Park(Place):
    def __str__(self):
        return f"Место проведения: Парк \"{self.place_title}\""


class Restaurant(Place):
    def __str__(self):
        return f"Место проведения: Ресторан \"{self.place_title}\""


class Event(ABC):  # Абстрактный класс типа мероприятия
    def __init__(self, event_date: date):
        self.event_date = event_date

    @abstractmethod
    def __str__(self):
        pass


class Birthday(Event):
    def __str__(self):
        return f"Тип мероприятия: День Рождения\nДата: {self.event_date}"


class Wedding(Event):
    def __str__(self):
        return f"Тип мероприятия: Свадьба\nДата: {self.event_date}"


class Staff(ABC):  # Абстрактный класс сотрудника
    def __init__(self, staff_amount: int):
        self.staff_amount = staff_amount

    @abstractmethod
    def __str__(self):
        pass


class Waiter(Staff):
    def __str__(self):
        return f"Сотрудник: Официант, количество: {self.staff_amount}"


class Photographer(Staff):
    def __str__(self):
        return f"Сотрудник: Фотограф, количество: {self.staff_amount}"


class EventCard:  # Класс карточки мероприятия
    def __init__(self, event: Event, place: Place, staff_list: list[Staff]):
        self.event = event
        self.place = place
        self.staff_list = staff_list

    def display_event_info(self):
        print(self.event, self.place, *self.staff_list, sep="\n", end="\n\n")


class PlaceFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_place(place_title: str):
        pass


class ParkFactory(PlaceFactory):
    @staticmethod
    def create_place(place_title: str):
        return Park(place_title)


class RestaurantFactory(PlaceFactory):
    @staticmethod
    def create_place(place_title: str):
        return Restaurant(place_title)


class EventFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_event(event_date: date):
        pass


class BirthdayFactory(EventFactory):
    @staticmethod
    def create_event(event_date: date):
        return Birthday(event_date)


class WeddingFactory(EventFactory):
    @staticmethod
    def create_event(event_date: date):
        return Wedding(event_date)


class StaffFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_staff(staff_amount: int):
        pass


class WaiterFactory(StaffFactory):
    @staticmethod
    def create_staff(staff_amount: int):
        return Waiter(staff_amount)


class PhotographerFactory(StaffFactory):
    @staticmethod
    def create_staff(staff_amount: int):
        return Photographer(staff_amount)


class EventRegistry:  # Менеджер расписания (Синглтон)
    _instance = None
    _lock = Lock()
    schedule = []

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def add_event(self, event_card: EventCard):
        self.schedule.append(event_card)

    def remove_event(self, event_card: EventCard):
        self.schedule.remove(event_card)

    def show_schedule(self):  # Выводит расписание мероприятий в порядке возрастания даты
        for i in sorted(self.schedule, key=lambda event_card: event_card.event.event_date):
            i.display_event_info()


def interact_with_user():
    # Создание первого мероприятия
    event_type1 = WeddingFactory.create_event(date(2026, 3, 21))
    place1 = RestaurantFactory.create_place("Пафосный дворик")
    staff1 = [WaiterFactory.create_staff(3), PhotographerFactory.create_staff(1)]
    event1 = EventCard(event_type1, place1, staff1)

    # Создание второго мероприятия
    event_type2 = BirthdayFactory.create_event(date(2023, 3, 21))
    place2 = ParkFactory.create_place("Покровский")
    staff2 = [StaffFactory.create_staff(1)]
    event2 = EventCard(event_type2, place2, staff2)

    # Добавление мероприятий в расписание и проверка правильности работы синглтона
    schedule1 = EventRegistry()
    schedule1.add_event(event1)
    schedule2 = EventRegistry()
    schedule2.add_event(event2)
    schedule1.show_schedule()


def main():
    interact_with_user()


if __name__ == "__main__":
    main()
