<template>

<Accordion value="0">
    <AccordionPanel value="0">
        <AccordionHeader>Initial Configuration</AccordionHeader>
        <AccordionContent>
            <p class="m-0">
                <Fieldset legend="Initial Configuration">
        <div class="card">
            <h3>Connection Configuration</h3>
            <p>Connection is a crucial thing that ensures proper operation.</p>

           
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
                </p>
        </AccordionContent>
    </AccordionPanel>
    <AccordionPanel value="1">
        <AccordionHeader>Header II</AccordionHeader>
        <AccordionContent>
            <p class="m-0">
                Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Consectetur, adipisci velit, sed quia non numquam eius modi.
            </p>
        </AccordionContent>
    </AccordionPanel>
    <AccordionPanel value="2">
        <AccordionHeader>Header III</AccordionHeader>
        <AccordionContent>
            <p class="m-0">
                At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa
                qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus.
            </p>
        </AccordionContent>
    </AccordionPanel>
</Accordion>














    <Card>
        <template #title>Simple Card</template>
        <template #content>
            <p class="m-0">
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore sed consequuntur error repudiandae
                numquam deserunt quisquam repellat libero asperiores earum nam nobis, culpa ratione quam perferendis
                esse, cupiditate neque
                quas!
            </p>
        </template>
    </Card>

</template>

<script setup>
import { ref } from 'vue';
import card from 'primevue/card';
import { RadioButton, Button, InputText } from 'primevue';
import Fieldset from 'primevue/fieldset';
import Accordion from 'primevue/accordion';
import AccordionPanel from 'primevue/accordionpanel';
import AccordionHeader from 'primevue/accordionheader';
import AccordionContent from 'primevue/accordioncontent';

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