from sqlalchemy import Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


engine = create_engine("sqlite:///student.db")
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    age: Mapped[int] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String)


def show_statistics() -> None:
    with SessionLocal() as session:
        total_students = session.scalar(select(func.count()).select_from(Student))
        average_age = session.scalar(select(func.avg(Student.age)))
        minimum_age = session.scalar(select(func.min(Student.age)))
        maximum_age = session.scalar(select(func.max(Student.age)))
        total_ages = session.scalar(select(func.sum(Student.age)))
        students_aged_17 = session.scalar(
            select(func.count()).select_from(Student).where(Student.age == 17)
        )
        atyrau_average_age = session.scalar(
            select(func.avg(Student.age)).where(Student.city == "Атырау")
        )

    print(f"Всего студентов: {total_students}")
    print(f"Средний возраст: {average_age}")
    print(f"Минимальный возраст: {minimum_age}")
    print(f"Максимальный возраст: {maximum_age}")
    print(f"Сумма возрастов: {total_ages}")
    print(f"Студентов 17 лет: {students_aged_17}")
    print(f"Средний возраст студентов из Атырау: {atyrau_average_age}")


def count_by_city(city: str) -> int:
    with SessionLocal() as session:
        count = session.scalar(
            select(func.count()).select_from(Student).where(Student.city == city)
        )

    return count or 0


if __name__ == "__main__":
    show_statistics()
