<template>
    <Fieldset legend="Initial Configuration">
        <div class="card">
            <h3>Connection Configuration</h3>
            <p>Connection is a crucial thing that ensures proper operation.</p>
            
            <hr />
            <br />
            <!-- Radio Buttons for Connection Methods -->
            <div class="field">
                <RadioButton id="standalone" style="margin-right: 10px;" v-model="connectionMethod"
                    value="standalone" />
                <label for="standalone" class="mr-2">Standalone configuration</label>

            </div>
            <div class="field">

                <RadioButton id="firstInSwarm" style="margin-right: 10px;" v-model="connectionMethod"
                    value="firstInSwarm" />
                <label for="firstInSwarm" class="mr-2">First in Swarm</label>
            </div>
            <div class="field">

                <RadioButton id="connectToSwarm" style="margin-right: 10px;" v-model="connectionMethod"
                    value="connectToSwarm" />
                <label for="connectToSwarm" class="mr-2">Connect to Swarm</label>
            </div>

            <!-- Conditional Content based on Connection Method -->
            <div v-if="connectionMethod === 'firstInSwarm'">
                <Button label="Create Swarm" icon="pi pi-plus" class="p-button-success mt-3" />
            </div>

            <div v-if="connectionMethod === 'connectToSwarm'">
                <div class="flex gap-4 mt-4">
                    <!-- IP Address Input -->
                    <div class="flex flex-column gap-2">
                        <label for="ipAddress">Enter IP Address</label>
                        <InputText id="ipAddress" v-model="ipAddress" placeholder="e.g., 192.168.1.1" />
                        <Button label="Connect" icon="pi pi-plug" class="p-button-primary" />
                    </div>

                    <!-- Subnet Scan Input -->
                    <div class="flex flex-column gap-2">
                        <label for="subnet">Scan Network</label>
                        <InputText id="subnet" v-model="subnet" placeholder="e.g., 192.168.1.0/24" />
                        <Button label="Scan" icon="pi pi-search" class="p-button-warning" />
                    </div>
                </div>
            </div>
        </div>
    </Fieldset>
</template>

<script setup>
import { ref } from 'vue';
import { RadioButton, Button, InputText } from 'primevue';
import Fieldset from 'primevue/fieldset';
const connectionMethod = ref(null);
const ipAddress = ref('');
const subnet = ref('');
</script>

<style scoped>
.card {
    width: 50%;
    margin: auto;
}

.field {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}

.flex {
    display: flex;
}

.flex-column {
    flex-direction: column;
}

.mt-3 {
    margin-top: 1rem;
}

.mt-4 {
    margin-top: 1.5rem;
}

.gap-2 {
    gap: 0.5rem;
}

.gap-4 {
    gap: 1rem;
}

.RadioButton {
    margin-right: 1rem;
}
</style>