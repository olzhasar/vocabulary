<template>
  <v-app id="inspire">
    <v-main>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-form @submit.prevent="login" ref="form">
              <h1>Vocabulary</h1>

              <v-text-field
                v-model="email"
                label="Email"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                append-icon="mdi-eye"
                type="password"
                label="Password"
                required
              ></v-text-field>

              <div class="red--text" v-if="this.$store.state.authError">
                {{ this.$store.state.authError }}
              </div>

              <v-btn color="info" class="mr-4" type="submit">
                Login
              </v-btn>
            </v-form>
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  data() {
    return {
      email: "",
      password: "",
      error: ""
    };
  },
  methods: {
    login: function() {
      const email = this.email;
      const password = this.password;
      this.$store.dispatch("login", { email, password });
    }
  }
});
</script>
