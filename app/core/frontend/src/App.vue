<template>
  <div id="app">
    <div id="nav">
      <router-link to="/subscription">Subscription</router-link> |
      <router-link v-on:click.native="resetNotifications()" to="/visualization">Visualization</router-link>
      <span v-if="notificationsCount !== 0" class="badge badge-pill badge-danger">{{ notificationsCount }}</span>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>

import store from './store'
import notificationApi from "./components/notification-api"

export default {
    name: 'app',
    data() {
      return {
        notificationsCount: 0
      }
    },
  methods: {
    startSchedulers: function () {
        setInterval(this.getNotifications, 5000);
    },
    getNotifications: function () {
      if (store.getters.isLoggedIn) {
        if ( this.$route.fullPath !== "/visualization") {
          notificationApi.getNotifications(store.getters.username).then(response => {
            let notifications = response.data;
            if (notifications) {
              this.notificationsCount = notifications.length;
            }
          }).catch(error => {
            console.log("Problem with server", error);
          });
        }
      }
    },
    resetNotifications: function () {
      this.notificationsCount = 0;
      this.$forceUpdate();
    }
  },
  mounted() {
      this.startSchedulers();
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

#nav {
  padding: 15px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
     color: #42b983;
    }
  }
}
</style>
