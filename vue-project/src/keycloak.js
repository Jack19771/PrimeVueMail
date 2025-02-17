import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
  url: "http://localhost:8080", // WAŻNE: bez `/auth`
  realm: "myrealm", // Musi się zgadzać z Keycloak
  clientId: "primevue-app" // Nazwa klienta w Keycloak
});

export default keycloak;
