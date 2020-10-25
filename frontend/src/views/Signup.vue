<template>
  <v-app id="inspire">
    <v-main>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-form @submit.prevent="signup" ref="form">
              <h1>Register account</h1>

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

              <div class="red--text" v-if="this.$store.state.authError">
                {{ this.error }}
              </div>

              <v-btn color="info" class="mr-4" type="submit">
                Register
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
      repeatPassword: "",
      error: ""
    };
  },
  methods: {
    signup: function() {
      const email = this.email;
      const password = this.password;
      const repeatPassword = this.repeatPassword;
      this.$store
        .dispatch("signup", { email, password, repeatPassword })
        .then(() => this.$router.push("/"))
        .catch(err => {
          if (err.response && err.response.status === 409) {
            this.error =
              "This email is already registered. Please, login instead";
          }
        });
    }
  }
});
</script>
