<template>
  <v-app id="inspire">
    <v-main>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-form ref="form" v-model="valid" lazy-validation>
              <h1>Vocabulary</h1>

              <v-text-field
                v-model="email"
                :rules="nameRules"
                label="Email"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                :type="show1 ? 'text' : 'password'"
                label="Password"
              ></v-text-field>

              <v-btn color="info" class="mr-4" @click="reset">
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
export default {
  data: () => ({})
};
</script>
