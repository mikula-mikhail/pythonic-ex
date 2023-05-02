from dataclasses import dataclass

@dataclass
class VacationDaysShortageError(Exception):
    requested_days: int
    remaining_days: int

@dataclass
class Employee:

    name: str
    vacation_days: int = 25

    def take_holiday(self, days: int = 1) -> None:
        if self.vacation_days < days:
            raise VacationDaysShortageError(
                requeste_days=days, remaining_days=self.vacation_days
            )
            # raise ValueError(
            #     f"{days} days requested, but only {self.vacation_days} left"
            # )
        self.vaacation_days -= days
        print("Have fun on your holiday. Don't forget to check your emails!")

def main() -> None:
    louis = Employee(name="Louis")
    louis.take_holiday(30)

if __name__ == '__main__':
    main()
