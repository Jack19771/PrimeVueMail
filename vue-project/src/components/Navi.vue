<template>
    <div class="card flex justify-center sidebar-container">
      <PanelMenu :model="items" class="w-full md:w-80">
        <template #item="{ item }">
          <div class="menu-item">
            <span :class="['menu-icon', item.icon, getStatusClass(item.status)]" />
            <span class="menu-label">{{ item.label }}</span>
            <span v-if="item.items" class="submenu-icon pi pi-angle-down" />
          </div>
        </template>
      </PanelMenu>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import PanelMenu from 'primevue/panelmenu';
  
  const items = ref([
    {
      label: 'SHAPE',
      icon: 'pi pi-arrow-circle-right',
      status: 'green',
      items: [
        {
          label: 'CMD Office',
          icon: 'pi pi-circle-fill',
          status: 'yellow',
          items: [
            {
              label: 'COS',
              icon: 'pi pi-file-pdf',
              items: [
                {
                  label: 'COS-IKM',
                  icon: 'pi pi-stop',
                  status: 'green'
                },
                {
                  label: 'COS-IMK',
                  icon: 'pi pi-check-circle',
                  status: 'red',
                  items: [
                    {
                      label: 'COS-IMK-1',
                      icon: 'pi pi-check-circle',
                      status: 'green'
                    },
                    {
                      label: 'COS-IMK-2',
                      icon: 'pi pi-check-circle',
                      status: 'red',
                      items: [
                        {
                          label: 'COS-IMK-2-1',
                          icon: 'pi pi-check-circle',
                          status: 'green'
                        },
                        {
                          label: 'COS-IMK-2-2',
                          icon: 'pi pi-check-circle',
                          status: 'red'
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]);
  
  const getStatusClass = (status) => {
    return {
      green: 'status-green',
      red: 'status-red',
      yellow: 'status-yellow'
    }[status] || '';
  };
  </script>
  
  <style scoped>
  /* Stylizacja kontenera Sidebar */
  .sidebar-container {
    position: fixed;
    top: 5;
    left: 0;
    width: 240px;
    height: 100vh;
    background-color: transparent;
    z-index: 1000;
    padding-top: 20px;
    padding-left: 20px;
  }
  
  .menu-item {
    display: flex;
    align-items: center;
    padding: 8px 16px;
    cursor: pointer;
    position: relative;
  }
  
  .menu-icon {
    font-size: 1.2rem;
    margin-right: 10px;
  }
  
  .menu-label {
    font-weight: 500;
  }
  
  .status-green {
    color: green;
  }
  
  .status-red {
    color: red;
  }
  
  .status-yellow {
    color: orange;
  }
  
  .submenu-icon {
    margin-left: auto;
    font-size: 1rem;
    color: var(--text-color-secondary);
  }
  </style>
  