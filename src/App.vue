<template>
  <div id="app">
    <app-frame>
      <router-view />
      
      <notifications group="default" />
    </app-frame>

  </div>
</template>

<script>
import AppFrame from './components/AppFrame.vue';

export default {
  components: {
    AppFrame
  }
}
</script>

<style>

</style>
