<template>
    <Accordion value="0">
        <AccordionPanel value="0">
            <AccordionHeader>Initial Configuration</AccordionHeader>
            <AccordionContent>
                <Fieldset legend="Initial Configuration">
                    <div class="card">
                        <h3>Connection Configuration</h3>
                        <p>Connection is a crucial thing that ensures proper operation.</p>

                        <!-- Radio Buttons for Connection Methods -->
                        <div class="field">
                            <RadioButton id="standalone" style="margin-right: 10px;" v-model="connectionMethod" value="standalone" />
                            <label for="standalone">Standalone configuration</label>
                        </div>
                        <div class="field">
                            <RadioButton id="firstInSwarm" style="margin-right: 10px;" v-model="connectionMethod" value="firstInSwarm" />
                            <label for="firstInSwarm">First in Swarm</label>
                        </div>
                        <div class="field">
                            <RadioButton id="connectToSwarm" style="margin-right: 10px;" v-model="connectionMethod" value="connectToSwarm" />
                            <label for="connectToSwarm">Connect to Swarm</label>
                        </div>

                        <!-- Uruchamianie pierwszego węzła -->
                        <div v-if="connectionMethod === 'firstInSwarm'">
                            <Button label="Create Swarm" icon="pi pi-plus" class="p-button-success mt-3" @click="startSwarm" />
                            <p v-if="swarmStatus" class="status-message">{{ swarmStatus }}</p>
                            <Button v-if="swarmRunning" label="Stop Swarm" icon="pi pi-times" class="p-button-danger mt-3" @click="stopSwarm" />
                        </div>

                        <!-- Dołączanie do istniejącego węzła -->
                        <div v-if="connectionMethod === 'connectToSwarm'">
                            <div class="flex gap-4 mt-4">
                                <div class="flex flex-column gap-2">
                                    <label for="ipAddress">Enter IP Address</label>
                                    <InputText id="ipAddress" v-model="ipAddress" placeholder="e.g., 192.168.1.1" />
                                    <Button label="Connect" icon="pi pi-plug" class="p-button-primary" @click="connectToSwarm" />
                                </div>
                            </div>
                        </div>
                    </div>
                </Fieldset>
            </AccordionContent>
        </AccordionPanel>
    </Accordion>
</template>

<script setup>
import { ref } from "vue";
import { Button, InputText, RadioButton } from "primevue";
import Fieldset from "primevue/fieldset";
import Accordion from "primevue/accordion";
import AccordionPanel from "primevue/accordionpanel";
import AccordionHeader from "primevue/accordionheader";
import AccordionContent from "primevue/accordioncontent";

const connectionMethod = ref(null);
const ipAddress = ref("");
const swarmStatus = ref(""); // Status węzła
const swarmRunning = ref(false); // Czy węzeł działa

// Uruchomienie pierwszego węzła
const startSwarm = async () => {
    try {
        const response = await fetch("http://localhost:8000/start-swarm", { method: "POST" });
        const data = await response.json();
        swarmStatus.value = data.message;
        swarmRunning.value = true;
    } catch (error) {
        swarmStatus.value = "Error starting swarm.";
    }
};

// Zatrzymanie węzła
const stopSwarm = async () => {
    try {
        const response = await fetch("http://localhost:8000/stop-swarm", { method: "POST" });
        const data = await response.json();
        swarmStatus.value = data.message;
        swarmRunning.value = false;
    } catch (error) {
        swarmStatus.value = "Error stopping swarm.";
    }
};

// Dołączenie do istniejącego węzła
const connectToSwarm = async () => {
    if (!ipAddress.value) {
        swarmStatus.value = "Enter a valid IP address.";
        return;
    }
    try {
        const response = await fetch(`http://localhost:8000/connect-swarm?ip=${ipAddress.value}`, { method: "POST" });
        const data = await response.json();
        swarmStatus.value = data.message;
    } catch (error) {
        swarmStatus.value = "Error connecting to swarm.";
    }
};
</script>

<style scoped>
.status-message {
    margin-top: 10px;
    font-weight: bold;
    color: green;
}
</style>
