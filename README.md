Wrzuciłem testowy skrypt do integracji Tauron - Home Assistant dla prosumentów uwzględniając rozłożenie 80/20.



Aby uruchomić ten kod w Home Assistant, należy wykonać następujące kroki:

Najpierw utwórz folder custom_components/tauron_sensor w katalogu konfiguracyjnym Home Assistant. W tym folderze utworzymy niezbędne pliki.

Skopiuj kod z oryginalnego main.py do pliku custom_components/tauron_sensor/tauron_api.py.

Dodaj konfigurację w pliku configuration.yaml:
# Nie jest wymagane dla config_flow, ale możesz dodać ręcznie:
tauron_sensor:
  username: twoj_login
  password: twoje_haslo

Zrestartuj Home Assistant.

Przejdź do Konfiguracja -> Integracje -> Dodaj integrację i wyszukaj "Tauron".

Wprowadź swoje dane logowania do Tauron eLicznik.

Po wykonaniu tych kroków, w Home Assistant pojawią się następujące sensory:

Dzienne zużycie energii
Dzienna produkcja energii
Bilans energii
Energia możliwa do odebrania
Energia magazynowana
Średnie godzinowe zużycie/produkcja
Szczytowe zużycie/produkcja i ich godziny

Sensory będą automatycznie aktualizowane co 15 minut. Możesz zmienić ten interwał modyfikując MIN_TIME_BETWEEN_UPDATES w pliku sensor.py.
Wszystkie sensory będą dostępne w panelu Home Assistant i możesz ich używać w automatyzacjach, kartach i dashboardach.
