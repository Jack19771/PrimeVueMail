<template>
    <Fieldset legend="Members">
        <p class="m-0">
            <OrganizationChart v-model:selectionKeys="selection" :value="data" collapsible selectionMode="multiple">
                <template #person="slotProps">
                    <div class="flex flex-col">
                        <div class="flex flex-col items-center">
                            <img :alt="slotProps.node.data.name" :src="slotProps.node.data.image"
                                class="mb-4 w-12 h-12" />
                            <span class="font-bold mb-2">{{ slotProps.node.data.name }}</span>
                            <span>{{ slotProps.node.data.title }}</span>
                        </div>
                    </div>
                </template>
                <template #default="slotProps">
                    <span>{{ slotProps.node.label }}</span>
                </template>
            </OrganizationChart>
        </p>
    </Fieldset>
</template>

<script setup>
import { ref } from "vue";
import Fieldset from 'primevue/fieldset';
import OrganizationChart from 'primevue/organizationchart';


const data = ref({
    key: '0',
    type: 'person',
    data: {
        image: 'https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png',
        name: 'Amy Elsner',
        title: 'CEO'
    },
    children: [
        {
            key: '0_0',
            type: 'person',
            data: {
                image: 'https://primefaces.org/cdn/primevue/images/avatar/annafali.png',
                name: 'Anna Fali',
                title: 'CMO'
            },
            children: [
                {
                    key: '0_0_0',
                    label: 'Sales'
                },
                {
                    key: '0_0_"1',
                    label: 'Marketing'
                }
            ]
        },
        {
            key: '0_1',
            type: 'person',
            data: {
                image: 'https://primefaces.org/cdn/primevue/images/avatar/stephenshaw.png',
                name: 'Stephen Shaw',
                title: 'CTO'
            },
            children: [
                {
                    key: '0_1_0',
                    label: 'Development'
                },
                {
                    key: '0_1_1',
                    label: 'UI/UX Design'
                }
            ]
        }
    ]
});
const selection = ref({});
</script>
