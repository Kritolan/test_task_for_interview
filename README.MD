# Решение тестового задания для одного из собеседований

В базовом решении сделал сортировку не по первому столбцу, а сразу по всем D столбцам,
из-за чего пришлось поправить референсные файлы

Для запуска тестов (требуется установленный nox):
```sh
$ nox
```
Для запуска скрипта:
```sh
$ poetry install
$ poetry run create_files
```

 Тесты сделаны минимально, без полного покрытия, проверяются только результаты,
 при необходимости их набор легко расширяется
 
 Все входные данные считываются кусочно и могут быть любого размера,
 но промежуточные данные хранятся в памяти, при необходимости их сохранения 
 или если памяти будет не хватать - можно добавить БД, тода расход памяти будет минимален
 
 По поводу некорректных данных - я никаких проверок не делал,
 подразумевая что данные все же не содержат ошибки. Т.к. данные формируются по идее автоматически - 
 то должен быть фиксированные набор возможных ошибок и уже по нему можно делать валидацию на этапе считывания
 
