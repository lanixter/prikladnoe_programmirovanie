# Ошибка 1
def get_age(self) -> int:
    now: datetime.datetime = datetime.datetime.now()
    return self.yob - now.year
# Ошибка 2
def set_name(self, name: str) -> None:
    self.name = self.name
# Ошибка 3
def set_address(self, address: str) -> None:
    self.address == address
# Ошибка 4
def is_homeless(self) -> bool:
    return address is None