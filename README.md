<h1>Hausnotruf</h1>
Dieses Skript liest in regelmäßigen Abständen die Anrufliste einer Fritzbox aus und kontrolliert, ob eine bestimmte Nummer angerufen wurde.
In diesem Moment sendet es über <a href=https://www.pushsafer.com>pushsafer</a> an die angegebenen Geräte. 
Dies kann zum Beispiel genutzt werden, um bei Hausnotrufen die Angehörigen direkt zu benachrichtigen.

<h2>Config</h2>
In der Config Datei muss die IP-Addresse der Fritzbox angegeben werden. 
Wenn sich der Computer, auf dem das Skript läuft, im selben Netzwerk ist, wie die Fritzbox (also selbes Subnetz), dann reicht das Passwort der Fritzbox. 
Wenn er sich z.B. über VPN mit der Fritzbox verbindet, muss ein Benutzer angegeben werden, der Berechtigung hat, sich aus der Ferne anzumelden.
Angegeben werden muss außerdem der Pushsafer-API-Key, die Pushsafer-Gruppe, die "Alarmiert" werden soll und eine Gruppe ("DeveloperMSG"), die bei Fehlern benachrichtigt werden soll. Dabei ist es wichtig, dass regelmäßig ein Fehler durch beenden der Session gesendet wird, dieser stellt aber kein tatsächliches Problem dar.<br>
"TestCallTime" Beschreibt die Zeit, zu der Testanrufe kommen. Ab diesem Zeitpunkt werden fünf Minuten lang Anrufe ignoriert. 
"isoweekdayTestCall" beschreibt den Tag, an dem der Testanruf kommt. Dabei ist Montag 1, Dienstag 2 usw.

<h2>Pushsafer</h2>
Pushsafer ist ein Programm, über das z.B. an Handys Pushnachrichten geschickt werden können. In diesem Fall werden kritische Nachrichten versendet, die auch den Stummodus umgehen.
Um dieses Programm zu nutzen, ist es nötig, dort einen Account zu erstellen, um einen API-Key zu erhalten, der genutzt wird, um eine Nachricht zu senden.
Außerdem können dort unter Geräte Gastgeräte hinzugefügt werden. Diesen können dann Gruppen zugewiesen werden. Die Nummern dieser Gruppen (ID) werden in der Konfiguration genutzt. 
