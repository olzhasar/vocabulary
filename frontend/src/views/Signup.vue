<template>
  <v-app id="inspire">
    <v-main>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <h1>Register account</h1>

            <v-form @submit.prevent="signup" ref="form">
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

              <v-text-field
                v-model="repeatPassword"
                append-icon="mdi-eye"
                type="password"
                label="Repeat password"
                required
              ></v-text-field>

              <div class="red--text" v-if="error">
                {{ error }}
              </div>

              <v-btn color="info" class="mr-4" type="submit">
                Register
              </v-btn>
            </v-form>

            <br />
            Already registered?
            <router-link to="/login">
              Login
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
      repeatPassword: "",
      error: ""
    };
  },
  methods: {
    signup: function() {
      if (this.password != this.repeatPassword) {
        this.error = "Passwords mismatch";
        return;
      }

      const email = this.email;
      const password = this.password;
      const repeatPassword = this.repeatPassword;
      this.$store
        .dispatch("signup", { email, password, repeatPassword })
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
