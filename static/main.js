//------------------------------------------------------------------------------
//Demonstrator evs/tco/tmg
//------------------------------------------------------------------------------
// rev. 1, 18.12.2020, Bm
// rev. 0, 21.11.2018, Bm
//------------------------------------------------------------------------------
// hier zur Vereinfachung (!) die Klassen in einer Datei

'use strict'

//------------------------------------------------------------------------------
class DetailView_cl {
//------------------------------------------------------------------------------

   constructor (el_spl, template_spl) {
      this.el_s = el_spl;
      this.template_s = template_spl;
   }
   render_px (id_spl) {
      // Daten anfordern
      let path_s = "/app/" + id_spl;
      let requester_o = new APPUTIL.Requester_cl();
      requester_o.GET_px(path_s)
      .then (result_spl => {
            this.doRender_p(JSON.parse(result_spl));
      })
      .catch (error_opl => {
         alert("fetch-error (get)");
      });
   }
   doRender_p (data_opl) {
      let markup_s = APPUTIL.tm_o.execute_px(this.template_s, data_opl);
      let el_o = document.querySelector(this.el_s);
      if (el_o != null) {
         el_o.innerHTML = markup_s;
         this.configHandleEvent_p();
      }
   }
   configHandleEvent_p () {
      let el_o = document.querySelector("form");
      if (el_o != null) {
         el_o.addEventListener("click", this.handleEvent_p);
      }
   }
   handleEvent_p (event_opl) {
      if (event_opl.target.id == "idBack") {
         APPUTIL.es_o.publish_px("app.cmd", ["idBack", null]);
         event_opl.preventDefault();
      }
   }
}

//------------------------------------------------------------------------------
class ListView_cl {
//------------------------------------------------------------------------------

   constructor (el_spl, template_spl, actionType) {
      this.el_s = el_spl;
      this.template_s = template_spl;
      this.configHandleEvent_p();
      this.actionType = actionType;
   }
   render_px (id) {
      // Daten anfordern
      let path_s = "/app/" + this.actionType + "/";
      if (id != null && id != -1){
         path_s = path_s + null + "/" + id + "/";
      }
      let requester_o = new APPUTIL.Requester_cl();
      requester_o.request_px(path_s,
          function (responseText_spl){
         let data_o = JSON.parse(responseText_spl);
         this.doRender_p(data_o);
          }.bind(this),
          function (responseText_spl){
         alert("List render fail");
          });
   }
   doRender_p (data_opl) {
      let markup_s = APPUTIL.tm_o.execute_px(this.template_s, data_opl);
      let el_o = document.querySelector(this.el_s);
      if (el_o != null) {
         el_o.innerHTML = markup_s;
      }
   }
   configHandleEvent_p () {
      let el_o = document.querySelector(this.el_s);
      if (el_o != null) {
         el_o.addEventListener("click", this.handleEvent_p);
      }
   }
   handleEvent_p (event_opl) {
      if (event_opl.target.tagName.toUpperCase() == "TD") {
         let elx_o = document.querySelector(".clSelected");
         if (elx_o != null) {
            elx_o.classList.remove("clSelected");
         }
         event_opl.target.parentNode.classList.add("clSelected");
         event_opl.preventDefault();
      }
   }
}

//------------------------------------------------------------------------------
class SideBar_cl {
//------------------------------------------------------------------------------

   constructor (el_spl, template_spl) {
      this.el_s = el_spl;
      this.template_s = template_spl;
      this.configHandleEvent_p();
   }
   render_px (data_opl) {
      let markup_s = APPUTIL.tm_o.execute_px(this.template_s, data_opl);
      let el_o = document.querySelector(this.el_s);
      if (el_o != null) {
         el_o.innerHTML = markup_s;
      }
   }
   configHandleEvent_p () {
      let el_o = document.querySelector(this.el_s);
      if (el_o != null) {
         el_o.addEventListener("click", this.handleEvent_p);
      }
   }
   handleEvent_p (event_opl) {
      let cmd_s = event_opl.target.dataset.action;
      APPUTIL.es_o.publish_px("app.cmd", [cmd_s, null]);
   }
}

class Application_cl {

   constructor () {
      // Registrieren zum Empfang von Nachrichten
      APPUTIL.es_o.subscribe_px(this, "templates.loaded");
      APPUTIL.es_o.subscribe_px(this, "templates.failed");
      APPUTIL.es_o.subscribe_px(this, "app.cmd");
      this.sideBar_o = new SideBar_cl("aside", "sidebar.tpl.html");



      //Pflege Mitarbeiter
      this.listview_mitarbeiter = new ListView_cl("main", "pflegeMitarbeiter.tpl.html", "mitarbeiter")
   }
   notify_px (self, message_spl, data_opl) {
      switch (message_spl) {
      case "templates.failed":
         alert("Vorlagen konnten nicht geladen werden.");
         break;
      case "templates.loaded":
         // Templates stehen zur Verfügung, Bereiche mit Inhalten füllen
         // hier zur Vereinfachung direkt
         let markup_s;
         let el_o;
         markup_s = APPUTIL.tm_o.execute_px("header.tpl.html", null);
         el_o = document.querySelector("header");
         if (el_o != null) {
            el_o.innerHTML = markup_s;
         }
         let nav_a = [
            ["home", "Startseite"],
            ["mitarbeiter", "Pflege Mitarbeiter"],
            ["weiterbildung", "Pflege Weiterbildung"],
            ["teilnahme_mitarbeiter", "Teilnahme Mitarbeiter"],
            ["teilnahme_weiterbildung", "Teilnahme Weiterbildung"],
            ["auswertung_mitarbeiter", "Auswertung Mitarbeiter"],
            ["auswertung_weiterbildung", "Auswertung Weiterbildung"],
            ["auswertung_zertifikat", "Auswertung Zertifikat"]
         ];
         self.sideBar_o.render_px(nav_a);
         //markup_s = APPUTIL.tm_o.execute_px("home.tpl.html", null);
         el_o = document.querySelector("main");
         if (el_o != null) {
            el_o.innerHTML = markup_s;
         }
         break;

      case "app.cmd":
         // hier müsste man überprüfen, ob der Inhalt gewechselt werden darf
         switch (data_opl[0]) {
         case "home":

            break;
         case "mitarbeiter":
            // Daten anfordern und darstellen
            this.listview_mitarbeiter.render_px(data_opl[1]);
            break;
         case "detail":
            this.detailView_o.render_px(data_opl[1]);
            break;
         case "idBack":
            APPUTIL.es_o.publish_px("app.cmd", ["list", null]);
            break;
         }
         break;
      }
   }
}

window.onload = function () {
   APPUTIL.es_o = new APPUTIL.EventService_cl();
   var app_o = new Application_cl();
   APPUTIL.createTemplateManager_px();
}