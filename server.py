# coding:utf-8

# Demonstrator es/te/tm

import sys
import os.path
import cherrypy

from app import application, template

#----------------------------------------------------------
def main():
#----------------------------------------------------------

   # aktuelles Verzeichnis ermitteln, damit es in der Konfigurationsdatei als
   # Bezugspunkt verwendet werden kann
   try:                                    # aktuelles Verzeichnis als absoluter Pfad
      currentDir_s = os.path.dirname(os.path.abspath(__file__))
   except:
      currentDir_s = os.path.dirname(os.path.abspath(sys.executable))
   cherrypy.Application.currentDir_s = currentDir_s

   configFileName_s = os.path.join(currentDir_s, 'server.conf') # im aktuellen Verzeichnis
   if os.path.exists(configFileName_s) == False:
      # Datei gibt es nicht
      configFileName_s = None

   # autoreload-Monitor hier abschalten
   cherrypy.engine.autoreload.unsubscribe()

   # 1. Eintrag: Standardverhalten, Berücksichtigung der Konfigurationsangaben im configFile
   cherrypy.tree.mount(
      None, '/', configFileName_s
   )

   # 2. Eintrag: Method-Dispatcher für die "Applikation" "app" vereinbaren
 #  cherrypy.tree.mount(
  #    application.Application_cl(),
   #   '/app',
    #  {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
  # )


# 2. Eintrag: Method-Dispatcher für die "Applikation" "app" vereinbaren
   cherrypy.tree.mount(
   application.Pflege_Mitarbeiter(),
   '/app/mitarbeiter',
   {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      application.mitarbeiter_detail_cl(),
      '/app/mitarbeiterAnzeigen/',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

# 2. Eintrag: Method-Dispatcher für "Weiterbildung"
   cherrypy.tree.mount(
      application.weiterbildung_detail_cl(),
      '/app/weiterbildungAnzeigen/',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   # 2. Eintrag: Method-Dispatcher für "Weiterbildung Anzeigen"
   cherrypy.tree.mount(
      application.Pflege_Weiterbildung(),
      '/app/weiterbildung/',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

# 2. Eintrag: Method-Dispatcher für "Teilnahme"
   cherrypy.tree.mount(
      application.Teilnahme_cl(),
      '/app/teilnahme/',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )
# 2. Eintrag: Method-Dispatcher für "Auswertung Mitarbeiter"
   cherrypy.tree.mount(
      application.Auswertung_Mitarbeiter(),
      '/app/auswertungMitarbeiter/',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   # 2. Eintrag: Method-Dispatcher für "Auswertung Weiterbildung"
   cherrypy.tree.mount(
      application.Auswertung_Weiterbildung(),
      '/app/auswertungWeiterbildung/',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   # 2. Eintrag: Method-Dispatcher für "Auswertung Zertifikate"
   cherrypy.tree.mount(
      application.Auswertung_Zertifikat(),
      '/app/auswertungZertifikat/',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   # 2. Eintrag: Method-Dispatcher für die "Applikation" "templates" vereinbaren
   cherrypy.tree.mount(
      template.Template_cl(),
      '/templates',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.engine.start()
   cherrypy.engine.block()

#----------------------------------------------------------
if __name__ == '__main__':
#----------------------------------------------------------
   main()