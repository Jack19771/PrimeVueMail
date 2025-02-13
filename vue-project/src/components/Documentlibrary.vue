<template>
    <div>
      <!-- Ribbon - pasek narzędzi -->
      <div v-if="selectedDocuments.length > 0" class="p-d-flex p-jc-between p-mb-3 p-ribbon">
        <Button label="View" icon="pi pi-search" @click="viewDocument" class="p-mr-2" />
        <Button label="Send To" icon="pi pi-send" @click="deleteDocuments" class="p-mr-2" />
        <Button label="Delete" icon="pi pi-trash" @click="deleteDocuments" class="p-mr-2" />
        <Button label="Edit" icon="pi pi-pencil" @click="editDocument" class="p-mr-2" />
      </div>
      <div>
 
      </div>
  
      <!-- Panel z tabelą dokumentów -->
      <Panel header="Document Library" class="p-mb-1">
        <div class="p-d-flex p-jc-between p-mb-3">
          <div>
            <Button label="Add Document" icon="pi pi-plus"   @click="addDocument" class="p-mr-2" />
          </div>
  
          <div>
            <InputText v-model="searchQuery" placeholder="Search documents..." class="p-inputtext p-component" />
          </div>
        </div>
  
        <!-- DataTable z dokumentami -->
        <div class="datatable-container">
          <DataTable  
            v-model:selection="selectedDocuments" 
            :value="filteredDocuments" 
            selectionMode="checkbox" 
            dataKey="id" 
            paginator 
            :rows="rowsPerPage" 
            :totalRecords="totalRecords" 
            :rowsPerPageOptions="[5, 10, 25]" 
            @page="onPageChange"
          >
            <Column selectionMode="multiple" ></Column>
            <Column field="name" header="Name" sortable></Column>
            <Column field="type" header="Type" sortable></Column>
            <Column field="area" header="Area" sortable></Column>
            <Column field="subArea" header="Sub-Area" sortable></Column>
            <Column header="Icon" :body="fileIconTemplate"></Column>
          </DataTable>
        </div>
      </Panel>
  
      <!-- Dialog do dodawania nowego dokumentu -->
      <Dialog header="Add Document" v-model:visible="dialogVisible" :style="{ width: '450px' }">
        <div>
          <InputText v-model="newDocument.name" placeholder="Document Name" class="p-inputtext p-component p-fluid" />
        </div>
        <div class="p-mt-3">
          <Dropdown v-model="newDocument.type" :options="documentTypes" placeholder="Select Document Type" class="p-dropdown p-component" />
        </div>
        <div class="p-mt-3">
          <InputText v-model="newDocument.icon" placeholder="Icon (e.g. pi pi-file-pdf)" class="p-inputtext p-component p-fluid" />
        </div>
        <div class="p-mt-3">
          <InputText v-model="newDocument.area" placeholder="Area" class="p-inputtext p-component p-fluid" />
        </div>
        <div class="p-mt-3">
          <InputText v-model="newDocument.subArea" placeholder="Sub-Area" class="p-inputtext p-component p-fluid" />
        </div>
  
        <div class="p-d-flex p-jc-end p-mt-4">
          <Button label="Cancel" icon="pi pi-times" @click="closeDialog" class="p-button-text p-mr-2" />
          <Button label="Save" icon="pi pi-check" @click="saveDocument" class="p-button-text" />
        </div>
      </Dialog>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Button from 'primevue/button';
  import InputText from 'primevue/inputtext';
  import Dropdown from 'primevue/dropdown';
  import Panel from 'primevue/panel';
  import Dialog from 'primevue/dialog';
  
  export default {
    components: {
      DataTable,
      Column,
      Button,
      InputText,
      Dropdown,
      Panel,
      Dialog
    },
    setup() {
      const documents = ref([
        { id: 1, name: 'Report.pdf', type: 'PDF', icon: 'pi pi-file-pdf', area: 'Finance', subArea: 'Accounting' },
        { id: 2, name: 'Presentation.pptx', type: 'PowerPoint', icon: 'pi pi-file-powerpoint', area: 'Marketing', subArea: 'Campaigns' },
        { id: 3, name: 'Invoice.docx', type: 'Word', icon: 'pi pi-file-word', area: 'Finance', subArea: 'Billing' },
        { id: 4, name: 'Document.txt', type: 'Text', icon: 'pi pi-file', area: 'Finance', subArea: 'Accounting' },
        { id: 5, name: 'Proposal.pdf', type: 'PDF', icon: 'pi pi-file-pdf', area: 'Marketing', subArea: 'Campaigns' }
      ]);
      const selectedDocuments = ref([]);
      const dialogVisible = ref(false);
      const searchQuery = ref('');
      const newDocument = ref({ name: '', type: '', icon: '', area: '', subArea: '' });
      const documentTypes = ref([
        { label: 'PDF', value: 'PDF' },
        { label: 'PowerPoint', value: 'PowerPoint' },
        { label: 'Word', value: 'Word' }
      ]);
      const rowsPerPage = ref(10);
      const totalRecords = ref(documents.value.length);
  
      // Filtracja dokumentów na podstawie zapytania
      const filteredDocuments = computed(() => {
        return documents.value.filter(doc => 
          doc.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
          doc.type.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          doc.area.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          doc.subArea.toLowerCase().includes(searchQuery.value.toLowerCase())
        );
      });
  
      // Funkcja generująca ikony plików
      const fileIconTemplate = (rowData) => {
        return `<i class="${rowData.icon}"></i>`;
      };
  
      // Funkcja otwierająca dialog do dodania dokumentu
      const addDocument = () => {
        dialogVisible.value = true;
      };
  
      // Funkcja zamykająca dialog
      const closeDialog = () => {
        dialogVisible.value = false;
      };
  
      // Funkcja zapisująca nowy dokument
      const saveDocument = () => {
        const newDoc = {
          id: documents.value.length + 1,
          name: newDocument.value.name,
          type: newDocument.value.type,
          icon: newDocument.value.icon,
          area: newDocument.value.area,
          subArea: newDocument.value.subArea,
        };
        documents.value.push(newDoc);
        dialogVisible.value = false;
      };
  
      // Funkcja usuwająca wybrane dokumenty
      const deleteDocuments = () => {
        documents.value = documents.value.filter(doc => !selectedDocuments.value.includes(doc));
        selectedDocuments.value = [];
      };
  
      // Funkcja wyświetlająca szczegóły dokumentu
      const viewDocument = () => {
        if (selectedDocuments.value.length > 0) {
          alert(`Viewing: ${selectedDocuments.value.map(doc => doc.name).join(', ')}`);
        }
      };
  
      // Funkcja edytująca dokument
      const editDocument = () => {
        if (selectedDocuments.value.length > 0) {
          alert(`Editing: ${selectedDocuments.value.map(doc => doc.name).join(', ')}`);
        }
      };
  
      // Funkcja obsługująca zmianę strony w tabeli
      const onPageChange = (event) => {
        rowsPerPage.value = event.rows;
      };
  
      return {
        documents,
        selectedDocuments,
        dialogVisible,
        searchQuery,
        newDocument,
        documentTypes,
        rowsPerPage,
        totalRecords,
        filteredDocuments,
        fileIconTemplate,
        addDocument,
        closeDialog,
        saveDocument,
        deleteDocuments,
        viewDocument,
        editDocument,
        onPageChange
      };
    }
  };
  </script>
  
  <style scoped>
  .p-datatable .p-datatable-thead > tr > th {
    text-align: center;
  }
  
  .datatable-container {
    margin-top: 20px;
  }
  
  .p-d-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .p-mt-3 {
    margin-top: 1rem;
  }
  
  .p-ribbon {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .p-ribbon button {
    margin-right: 10px;
  }





  </style>
  