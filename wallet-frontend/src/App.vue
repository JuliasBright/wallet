<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <EndpointList/>
</template>

<script>
import EndpointList from './components/EndpointList.vue'

export default {
  name: 'App',
  components: {
    EndpointList
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
