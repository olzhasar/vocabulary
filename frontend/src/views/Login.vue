<template>
  <v-app id="inspire">
    <v-main>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <h1>Vocabulary</h1>

            <v-form @submit.prevent="login" ref="form">
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

              <div class="red--text" v-if="error">
                {{ error }}
              </div>

              <v-btn color="info" class="mr-4" type="submit">
                Login
              </v-btn>
            </v-form>

            <br />
            Don't have an account yet?
            <router-link to="/signup">
              Sign up
            </router-link>
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
      this.$store
        .dispatch("login", { email, password })
        .then(() => {
          this.$router.push("/");
        })
        .catch(err => {
          this.error = err;
        });
    }
  }
});
</script>
