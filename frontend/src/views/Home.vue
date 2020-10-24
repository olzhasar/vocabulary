<template>
  <div class="home">
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md6>
          <div class="text-h5 text-center mb-6">Vocabulary</div>
          <search></search>

          <div v-if="this.$store.state.words.length">
            <div class="text-h6 text-center mb-3">Saved words</div>

            <v-expansion-panels v-if="this.$store.state.words.length">
              <v-expansion-panel
                v-for="word in this.$store.state.words"
                :key="word.id"
              >
                <v-expansion-panel-header>
                  {{ word.name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-list-item
                    v-for="variant in word.variants"
                    :key="variant.id"
                  >
                    <v-list-item-content>
                      <v-list-item-title>
                        {{ variant.definition }}
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        {{ variant.part_of_speech }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import search from "../components/Search.vue";

export default Vue.extend({
  data() {
    return {
      words: [],
      searched: {
        name: null,
        data: {}
      }
    };
  },
  components: {
    search
  },
  methods: {
    loadWords: function() {
      this.$store.dispatch("getWords");
    }
  },
  mounted() {
    this.loadWords();
  }
});
</script>
