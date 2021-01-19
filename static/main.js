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

   constructor (el_spl, template_spl, actionType) {
      this.el_s = el_spl;
      this.template_s = template_spl;
      this.actionType = actionType;

   }
   render_px (id_spl,isW) {
      // Daten anfordern

      let path_s = "/app/" +this.actionType+"/" +id_spl;
      if (isW !== undefined){
         path_s = "/app/" +this.actionType+"/" +id_spl +"/" +isW;
      }
      console.log("render_px | path_s = " + path_s);
      let requester_o = new APPUTIL.Requester_cl();
      requester_o.request_px(path_s,
         function (responseText_spl) {
            let data_o = JSON.parse(responseText_spl);   //hole Json daten aus View.py
            this.doRender_p(data_o);   //übergebe die Daten an die Renderfunktion
         }.bind(this),
         function (responseText_spl) {
            alert("Anzeigen - render failed");
         }
      );
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

      let applybtn = document.querySelector(".anmelden");
      let cancelbtn = document.querySelector(".stornieren");

      let bckbtnemployee = document.querySelector(".zurückmitarbeiter");
      let bckbtntraining = document.querySelector(".zurückweiterbildung");

      let bckbtnresemployee = document.querySelector(".zurück_auswertung_mitarbeiter");
      let bckbtnrestraining = document.querySelector(".zurück_auswertung_weiterbildung"); // Auswertung: Weiterbildung anzeigen
      let bckbtnrescerts = document.querySelector(".zurück_auswertung_zertifikat");

      let btnsucces = document.querySelector(".erfolg");    // Erfolg
      let btnfail = document.querySelector(".nichterfolg");    // NichtErfolg
      let btncancel = document.querySelector(".abbruch");

      if (applybtn != null) {
         console.log("c: this.action = " + this.action);
         applybtn.addEventListener("click", this.handleEvent_p);
      }

      //EventListener wird gesetzt
      if (cancelbtn != null) {
         console.log("c: this.action = " + this.action);
         cancelbtn.addEventListener("click", this.handleEvent_p);
      }

      //EventListener wird gesetzt
      if (bckbtnemployee != null) {
         console.log("c: this.action = " + this.action);
         bckbtnemployee.addEventListener("click", this.handleEvent_p);
      }

      //EventListener wird gesetzt
      if (bckbtntraining != null) {
         console.log("c: this.action = " + this.action);
         bckbtntraining.addEventListener("click", this.handleEvent_p);
      }

      //EventListener wird gesetzt
      if (bckbtnresemployee != null) {
         console.log("c: this.action = " + this.action);
         bckbtnresemployee.addEventListener("click", this.handleEvent_p);
      }

      //EventListener wird gesetzt
      if (bckbtnrestraining != null) {
         console.log("c: this.action = " + this.action);
         bckbtnrestraining.addEventListener("click", this.handleEvent_p);
      }

      //EventListener wird gesetzt
      if (bckbtnrescerts != null) {
         console.log("c: this.action = " + this.action);
         bckbtnrescerts.addEventListener("click", this.handleEvent_p);
      }
        //EventListener wird gesetzt
      if (btnsucces != null) {
         console.log("c: this.action = " + this.action);
         btnsucces.addEventListener("click", this.handleEvent_p);
      }

      //EventListener wird gesetzt
      if (btnfail != null) {
         console.log("c: this.action = " + this.action);
         btnfail.addEventListener("click", this.handleEvent_p);
      }

      //EventListener wird gesetzt
      if (btncancel != null) {
         console.log("c: this.action = " + this.action);
         btncancel.addEventListener("click", this.handleEvent_p);
      }


      }
   handleEvent_p (event_opl) {
      if (event_opl.target.tagName.toUpperCase() == "TD") { //falls eine Tabellenzeile ausgewählt wurde, setzte eine ID. Auf diese ID können die anderen events zugreifen, um so die ID der Tabellenzeile zu erhalten, z.b. die Mitarbeiter-ID
         let elx_o = document.querySelector(".clSelected");
            if (elx_o != null) {
               elx_o.classList.remove("clSelected");
            }
         event_opl.target.parentNode.classList.add("clSelected");
         event_opl.preventDefault();
      }

      //Zurückbuttons
      else if (event_opl.target.id == "idBackmitarbeiter") {
         APPUTIL.es_o.publish_px("app.cmd", ["idBackmitarbeiter", null]);
         event_opl.preventDefault();
      }

      //Zurückbuttons
      else if (event_opl.target.id == "idBackweiterbildung") {
         APPUTIL.es_o.publish_px("app.cmd", ["idBackweiterbildung", null]);
         event_opl.preventDefault();
      }

      //Zurückbuttons
      else if (event_opl.target.id == "idBackAuswertungMitarbeiter") {
         APPUTIL.es_o.publish_px("app.cmd", ["idBackAuswertungMitarbeiter", null]);
         event_opl.preventDefault();
      }

      //Zurückbuttons
      else if (event_opl.target.id == "idBackAuswertungWeiterbildung") {
         APPUTIL.es_o.publish_px("app.cmd", ["idBackAuswertungWeiterbildung", null]);
         event_opl.preventDefault();
      }

      //Zurückbuttons
      else if (event_opl.target.id == "idBackAuswertungZertifikat") {
         APPUTIL.es_o.publish_px("app.cmd", ["idBackAuswertungZertifikat", null]);
         event_opl.preventDefault();
      } //teilnahme in teilnahme mitarbeiter anzeigen
      else if ( event_opl.target.id == "idSaveTeilnahme"){
          //doppelte anmeldung bei trainings möglich, mitarbeiterid ans ende jedes geplanten
         // trainings. setzten in der tpl, wenn id und selected gleich dann auswahl ungültig
         var elx = document.querySelector(".clSelected");   //ID von Tabellenzeile wird abgefragt
         var mitarbeiterdaten = document.getElementById("mitid").dataset.value;  //hole Mitarbeiter-ID von der Tpl Datei
         if (elx == null || elx.id == mitarbeiterdaten) {  //Falls kein Tabelleneintrag ausgewählt wurde oder der ausgewählte Tabelleneintrag == der MitarbeiterID ist, dann blockiere. (Man kann sich für keinen Mitarbeiter anmelden. Nur für eine Weiterbildung :))

            alert("Bitte zuerst einen gültigen Eintrag auswählen!");
         }
         else {
            APPUTIL.es_o.publish_px("app.cmd", ["addteilnahme", elx.id, mitarbeiterdaten] );  //rufe addteilnahme auf und übergebe die Weiterbildungs-ID und die Mitarbeiter-ID. Funktion läuft über publish_px in evs.js. Von dort wird die notify_px in main.js aufgerufen. Dort muss ein case und eine Funktion mit "addteilnahme" existieren. Und dort wird es dann in die Application.py übergeben mit dem Befehel POST.
         }
      } //teilnahme stornieren in teilnahme mitarbeiter
      else if ( event_opl.target.id == "idDeleteTeilnahme"){
         var elx = document.querySelector(".clSelected");

         var mitarbeiterdaten = document.getElementById("mitid").dataset.value;  //hole Mitarbeiter-ID von der Tpl Datei
         if (elx== null || elx.id == mitarbeiterdaten) {  //Falls kein Tabelleneintrag ausgewählt wurde oder der ausgewählte Tabelleneintrag == der MitarbeiterID ist, dann blockiere. (Man kann keinen Mitarbeiter stornieren. Nur eine Weiterbildung :))

            alert("Bitte zuerst einen gültigen Eintrag auswählen!");
         }
         else {
            APPUTIL.es_o.publish_px("app.cmd", ["deleteteilnahme", elx.id, mitarbeiterdaten] );  //rufe deleteteilnahme auf und übergebe die Weiterbildungs-ID und die Mitarbeiter-ID. Funktion läuft über publish_px in evs.js. Von dort wird die notify_px in main.js aufgerufen. Dort muss ein case und eine Funktion mit "deleteteilnahme" existieren. Und dort wird es dann in die Application.py übergeben mit dem Befehel DELETE.
         }
      }else if (event_opl.target.id == "erfolgTeilnahme"){
         var elx = document.querySelector(".clSelected");   //ID von Tabellenzeile wird abgefragt
         var weiterbildungdaten = document.getElementById("weiid").dataset.value;  //hole Weiterbildung-ID von der Tpl Datei
         if (elx == null || elx.id == weiterbildungdaten) {   //Falls kein Tabelleneintrag ausgewählt wurde oder der ausgewählte Tabelleneintrag == der WeiterbildungsID ist, dann blockiere. (Man kann den Status nur für Mitarbeiter ändern, nicht für eine Weiterbildung :))

            alert("Bitte zuerst einen gültigen Eintrag auswählen!");
         }
         else {
            status = "erfolgreich";
            APPUTIL.es_o.publish_px("app.cmd", ["erfolgTeilnahme", elx.id, weiterbildungdaten, status]);  //übergebe die Mitarbeiter-ID und die WeiterbildungsID, sowie den Status
         }
      }else if (event_opl.target.id == "nichterfolgTeilnahme"){
         var elx = document.querySelector(".clSelected");   //ID von Tabellenzeile wird abgefragt
         var weiterbildungdaten = document.getElementById("weiid").dataset.value;  //hole Weiterbildung-ID von der Tpl Datei
         if (elx == null || elx.id == weiterbildungdaten) {   //Falls kein Tabelleneintrag ausgewählt wurde oder der ausgewählte Tabelleneintrag == der WeiterbildungsID ist, dann blockiere. (Man kann den Status nur für Mitarbeiter ändern, nicht für eine Weiterbildung :))

            alert("Bitte zuerst einen gültigen Eintrag auswählen!");
         }
         else {
            status = "nicht erfolgreich";
            APPUTIL.es_o.publish_px("app.cmd", ["nichterfolgTeilnahme", elx.id, weiterbildungdaten, status]);   //übergebe die Mitarbeiter-ID und die WeiterbildungsID, sowie den Status
         }
      } else if (event_opl.target.id == "abbruchTeilnahme"){
         var elx = document.querySelector(".clSelected");   //ID von Tabellenzeile wird abgefragt
         var weiterbildungdaten = document.getElementById("weiid").dataset.value;  //hole Weiterbildung-ID von der Tpl Datei
         if (elx == null || elx.id == weiterbildungdaten) {   //Falls kein Tabelleneintrag ausgewählt wurde oder der ausgewählte Tabelleneintrag == der WeiterbildungsID ist, dann blockiere. (Man kann den Status nur für Mitarbeiter ändern, nicht für eine Weiterbildung :))

            alert("Bitte zuerst einen gültigen Eintrag auswählen!");
         }
         else {
            status = "abgebrochen";
            APPUTIL.es_o.publish_px("app.cmd", ["abbruchTeilnahme", elx.id, weiterbildungdaten, status]); //übergebe die Mitarbeiter-ID und die WeiterbildungsID, sowie den Status
         }
      }


   }
}



class FormView_cl{
   constructor(el_spl,template_spl, actionType, methodt) {
      this.el_s = el_spl;
      this.template_s = template_spl;
      this.actionType = actionType
      this.methodt = methodt;
   }

   render_px (id,typ) {
      // Daten anfordern
      let path_s = "/app/" + this.actionType + "/" + id;
      if (typ != undefined){
         path_s = path_s + "/" + typ;
      }
      let requester_o = new APPUTIL.Requester_cl();
      requester_o.request_px(path_s,
          function (responseText_spl){

         let data_o = JSON.parse(responseText_spl);
         data_o.id = id;
         this.doRender_p(data_o);
          }.bind(this),
          function (responseText_spl){
         alert("Form render fail");
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

   configHandleEvent_p(){
      let el_o = document.querySelector("form");
      if (el_o != null){
         el_o.addEventListener("click", this.handleEvent_p.bind(this));
      }
   }


   handleEvent_p(event_a){

      if (event_a.target.id == "idBack")
      {
         APPUTIL.es_o.publish_px("app.cmd",["idBack",null]);
         event_a.preventDefault();
      }
      else if (event_a.target.id == "idSave"){
         let data_o = {};
         var form = document.getElementById("idForm");
         var input_type = document.getElementById("action");
         var para = new URLSearchParams(new FormData(form));
         let url = "/app/"+input_type.value + "/";

         let METHOD = this.methodt;



         fetch(url, {method: METHOD, body: para, header: {"Content-type": "application/x-www-form-urlencoded"}}).then(res => res.json())
             .then(response => console.log("SUCCESS!ID=",response,alert("Speichern erfolgreich"), APPUTIL.es_o.publish_px("app.cmd",["input_type", response])))
             .catch(error => console.error("Error", error));

         APPUTIL.es_o.publish_px("app.cmd", ["idSave", null]);
         event_a.preventDefault();
      }
   }
}
//------------------------------------------------------------------------------
class ListView_cl {
//------------------------------------------------------------------------------

   constructor (el_spl, template_spl, actionType, method) {
      this.el_s = el_spl;
      this.template_s = template_spl;

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
      this.configHandleEvent_p();
      if (el_o != null) {
         el_o.innerHTML = markup_s;

      }
   }
   configHandleEvent_p () {
      let el_o = document.querySelector(this.el_s);
      if (el_o != null) {
         el_o.addEventListener("click", this.handleEvent_px);
      }
   }
   handleEvent_px (event_opl) {
      //Auswahl zeile

      if (event_opl.target.tagName.toUpperCase() == "TD") {
         let elx_o = document.querySelector(".clSelected");
         if (elx_o != null) {
            elx_o.classList.remove("clSelected");
         }
         event_opl.target.parentNode.classList.add("clSelected");
         //event_opl.target.classList.add("clSelected");

         event_opl.preventDefault();
      }

      else if (event_opl.target.id == "mitarbeiter"){
         APPUTIL.es_o.publish_px("app.cmd", ["mitarbeiter", null]);
      }
      //Erfassen mitarbeiter
      else if ( event_opl.target.id == "erfassen_mitarbeiter"){
         let method = document.getElementById("methodPOST")
         APPUTIL.es_o.publish_px("app.cmd", ["form_mitarbeiter", null, "","POST"]);
      }
      //Bearbeiten Mitabeiter
      else if (event_opl.target.id == "bearbeiten_mitarbeiter"){
         let method = document.getElementById("methodPUT")

         let elx = document.querySelector(".clSelected");
         if (elx == null){
            alert("bitte eintrag wählen");

         }else {
            APPUTIL.es_o.publish_px("app.cmd", ["form_mitarbeiter", elx.id,null,"PUT"]);
         }

      }//Erfassen training
      else if (event_opl.target.id == "erfassen_weiterbildung"){
            APPUTIL.es_o.publish_px("app.cmd", ["form_weiterbildung", null,"","POST"]);
         }//liste training
      else if (event_opl.target.id == "weiterbildung"){
         APPUTIL.es_o.publish_px("app.cmd", ["weiterbildung", null]);
      }
      else if( event_opl.target.id == "bearbeiten_weiterbildung"){
         let elx = document.querySelector(".clSelected");
         if (elx == null) {

            alert("Bitte Eintrag auswählen!");
         }else {

            console.log("bearbeiten_weiterbildung");
            APPUTIL.es_o.publish_px("app.cmd", ["form_weiterbildung", elx.id] );
         }
      }

      //detailmitarbeiter
      else if (event_opl.target.id == "anzeigen_mitarbeiter"){
         console.log(event_opl.target.tagName)
         let elx = document.querySelector(".clSelected");
         if (elx == null) {

            alert("Bitte zuerst einen Eintrag auswählen!");
         }else {

            console.log("anzeigen_mitarbeiter");
            APPUTIL.es_o.publish_px("app.cmd", ["anzeigen_mitarbeiter", elx.id] );
         }
      }
      else if (event_opl.target.id == "idDelete"){
         let elx = document.querySelector(".clSelected");
         if (elx == null)
         {
            alert("bitte eintrag wählen")
         }else {
            APPUTIL.es_o.publish_px("app.cmd", ["idDelete", elx.id]);
         }
      } else if (event_opl.target.id == "anzeigen_weiterbildung"){
         let elx = document.querySelector(".clSelected");
         if (elx == null)
         {
            alert("bitte eintrag wählen");
         }else {
            APPUTIL.es_o.publish_px("app.cmd", ["anzeigen_weiterbildung", elx.id]);
         }
         //Teilnahme Mitarbeiter anzeigen
      } else if (event_opl.target.id == "anzeigen_teilnahme_mitarbeiter"){
         let elx = document.querySelector(".clSelected");
         if (elx == null){
            alert("bitte eintrag wählen");
         }else{
            APPUTIL.es_o.publish_px("app.cmd",["anzeigen_teilnahme_mitarbeiter",elx.id]);
         }
         //teilnahme weiterbildung anzeigen
      }else if (event_opl.target.id == "anzeigen_teilnahme_weiterbildung"){
         let elx_o = document.querySelector(".clSelected");
         if (elx_o == null) {

            alert("Bitte zuerst einen Eintrag auswählen!");
         }else {

            console.log("anzeigen_teilnahme_weiterbildung");
            APPUTIL.es_o.publish_px("app.cmd", ["anzeigen_teilnahme_weiterbildung", elx_o.id, "isW"] );
         }
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

      var m = document.getElementsByTagName("main");
         m.id = btoa("main")

      //Pflege Mitarbeiter
      this.listview_mitarbeiter = new ListView_cl("main", "pflegeMitarbeiter.tpl.html", "mitarbeiter");
      this.FormView_mitarbeiterPUT = new FormView_cl("main","formMitarbeiter.tpl.html","mitarbeiter", "PUT");
      this.FormView_mitarbeiterPOST = new FormView_cl("main","formMitarbeiter.tpl.html","mitarbeiter", "POST");
      this.DetailView_Mitarbeiter = new DetailView_cl("main", "detailMitarbeiter.tpl.html", "mitarbeiterAnzeigen")
      //Pflege weiterbildung
      this.listview_weiterbildung = new ListView_cl("main", "pflegeWeiterbildungen.tpl.html", "weiterbildung");
      this.FormView_weiterbildungPOST = new FormView_cl("main", "formWeiterbildung.tpl.html","weiterbildung","POST");
      this.FormView_weiterbildungPUT = new FormView_cl("main", "formWeiterbildung.tpl.html","weiterbildung", "PUT");
      this.DetailView_weiterbildung = new DetailView_cl("main", "detailWeiterbildung.tpl.html", "weiterbildungAnzeigen");
        //Teilnahme Mitarbeiter
      this.listview_teilnahme_mitarbeiter = new ListView_cl("main", "TeilnahmeMitarbeiter.tpl.html", "mitarbeiter");
      this.DetailView_teilnahme_mitarbeiter = new DetailView_cl("main", "TeilnahmeMitarbeiterAnzeige.tpl.html", "teilnahme");
      //Teilnahme Weiterbildung
      this.listView_teilnahme_weiterbildung = new ListView_cl("main", "TeilnahmeWeiterbildung.tpl.html", "weiterbildung");
      this.DetailView_teilnahme_weiterbildung = new DetailView_cl("main", "TeilnahmeWeiterbildungAnzeige.tpl.html", "teilnahme");
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
                this.listview_mitarbeiter.render_px(data_opl[1]);
                break;


            case "form_mitarbeiter":
             if ( data_opl[3] == "POST")
               {
                this.FormView_mitarbeiterPOST.render_px(data_opl[1],data_opl[2]);
                }else{
                  this.FormView_mitarbeiterPUT.render_px(data_opl[1],data_opl[2]);

               }
               break;


            case "weiterbildung":
               this.listview_weiterbildung.render_px(data_opl[1]);
               break;


            case "form_weiterbildung":
               if (data_opl[3] == "POST"){
                  this.FormView_weiterbildungPOST.render_px(data_opl[1],data_opl[2]);

               }else {
                  this.FormView_weiterbildungPUT.render_px(data_opl[1],data_opl[2]);
               }
               break;
            //teilnahme mitarbeiter
            case "teilnahme_mitarbeiter":
               this.listview_teilnahme_mitarbeiter.render_px(data_opl[1]);
               break;
            case "anzeigen_teilnahme_mitarbeiter":
               this.DetailView_teilnahme_mitarbeiter.render_px(data_opl[1], data_opl[2]);
               break;
            case "addteilnahme":
               var url = "/app/" +"teilnahme" + "/" + data_opl[1] + "/" + data_opl[2];
               fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'} })
      				APPUTIL.es_o.publish_px("app.cmd", ["teilnahme_mitarbeiter", null]);
               break;
            case "deleteteilnahme":
               var url = "/app/" +"teilnahme" + "/" + data_opl[1] + "/" + data_opl[2];
               fetch(url, {method: 'DELETE', headers: {'Content-Type': 'application/json'} })
      				APPUTIL.es_o.publish_px("app.cmd", ["teilnahme_mitarbeiter", null]);
               break;



             //teilnahme weiterbildung
            case "teilnahme_weiterbildung":
               this.listView_teilnahme_weiterbildung.render_px(data_opl[1])
               break;
            case "anzeigen_teilnahme_weiterbildung":
               this.DetailView_teilnahme_weiterbildung.render_px(data_opl[1], data_opl[2]);
               break;
            //Status
            case "erfolgTeilnahme":
               var url = "/app/" + "teilnahme" + "/" + data_opl[1] + "/" + data_opl[2] + "/" + data_opl[3];   // 1. Mitarbeiter, 2. Weiterbildung, 3. Status
                  fetch(url, {method: 'PUT', headers: {'Content-Type': 'application/json'} })
      				APPUTIL.es_o.publish_px("app.cmd", ["teilnahme_weiterbildung", null]);
               break;
            case "nichterfolgTeilnahme":
               var url = "/app/" + "teilnahme" + "/" + data_opl[1] + "/" + data_opl[2] + "/" + data_opl[3];   // 1. Mitarbeiter, 2. Weiterbildung, 3. Status
                  fetch(url, {method: 'PUT', headers: {'Content-Type': 'application/json'} })
      				APPUTIL.es_o.publish_px("app.cmd", ["teilnahme_weiterbildung", null]);
               break;
            case "abbruchTeilnahme":
               var url = "/app/" + "teilnahme" + "/" + data_opl[1] + "/" + data_opl[2] + "/" + data_opl[3];   // 1. Mitarbeiter, 2. Weiterbildung, 3. Status
                  fetch(url, {method: 'PUT', headers: {'Content-Type': 'application/json'} })
      				APPUTIL.es_o.publish_px("app.cmd", ["teilnahme_weiterbildung", null]);
               break;

            case "idBack":
               var input_type = document.getElementById("action");
               APPUTIL.es_o.publish_px("app.cmd", [input_type.value, null]);
               break;
            case "anzeigen_mitarbeiter":
               this.DetailView_Mitarbeiter.render_px(data_opl[1]);
               break;
            case "anzeigen_weiterbildung":
               this.DetailView_weiterbildung.render_px(data_opl[1]);
               break;
            case "idBackmitarbeiter":
               APPUTIL.es_o.publish_px("app.cmd", ["mitarbeiter", null]);
               break;
            case "idBackweiterbildung":
               APPUTIL.es_o.publish_px("app.cmd", ["weiterbildung",null]);
               break;
            case "idDelete":
               if (confirm("Entfernen?")){
                  var input_type = document.getElementById("action");
                  var url = "/app/" + input_type.value + "/" + data_opl[1];
                  fetch(url, {method: 'DELETE', headers: {'Content-Type': 'application/json'} })
      				   APPUTIL.es_o.publish_px("app.cmd", [input_type.value, null]);
               }

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