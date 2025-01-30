<template>
  <Toolbar style="position: fixed; top: 0; left: 0; right: 0; z-index: 9999; border-radius: 0; padding: 1rem; background: linear-gradient(to top, #505050 , #000000);">
    <template #start>
      <div class="flex items-center gap-2">
        <!-- Logo FastTrack2 i Ikona maila -->
        <router-link to="/" style="display: flex; align-items: center;">
  <i class="pi pi-envelope" style="font-size: 2rem; color: #ffffff;"></i>
  <h3 style="margin-left: 10px; color: #ffffff; font-size: 1.5rem; font-weight: bold;">FastTrack 2</h3>
</router-link>

      </div>
    </template>

    <template #end>
      <div class="flex items-center gap-2">
        <!-- Użyj router-link zamiast Button do nawigacji -->
        <router-link to="/settings">
          <Button label="Settings" severity="contrast" size="small" />
        </router-link>
        <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" style="width: 32px; height: 32px" />
      </div>
    </template>
  </Toolbar>
</template>

<script setup>
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import Avatar from 'primevue/avatar';
</script>

<style scoped>
/* Flexbox dla umiejscowienia elementów */
.flex {
  display: flex;
  align-items: center;
}
</style>
