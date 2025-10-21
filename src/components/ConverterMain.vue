<template>
  <v-container class="converter-main">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="4" class="pa-4">
          <v-card-title class="text-h5 text-center mb-4">
            Computer Unit Converter
          </v-card-title>

          <v-card-text>
            <!-- Input Section -->
            <v-row>
              <v-col cols="12" md="6">
                <v-card outlined class="pa-4">
                  <v-card-subtitle class="text-subtitle-2 mb-2">From</v-card-subtitle>

                  <v-text-field
                    :model-value="store.inputValue"
                    @update:model-value="store.setInputValue"
                    label="Enter value"
                    type="number"
                    variant="outlined"
                    density="comfortable"
                    hide-details="auto"
                    class="mb-4"
                  />

                  <v-select
                    :model-value="store.fromUnit"
                    @update:model-value="store.setFromUnit"
                    :items="store.availableFromUnits"
                    item-title="label"
                    item-value="key"
                    return-object
                    label="Select unit"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item v-bind="props">
                        <template v-slot:subtitle>
                          <span class="text-caption">{{ item.raw.description }}</span>
                        </template>
                      </v-list-item>
                    </template>
                  </v-select>
                </v-card>
              </v-col>

              <!-- Swap Button -->
              <v-col cols="12" md="12" class="d-flex align-center justify-center py-2">
                <v-btn
                  icon="mdi-swap-horizontal"
                  color="primary"
                  variant="tonal"
                  @click="store.swapUnits"
                  :disabled="!store.fromUnit || !store.toUnit"
                />
              </v-col>

              <!-- Output Section -->
              <v-col cols="12" md="6">
                <v-card outlined class="pa-4">
                  <v-card-subtitle class="text-subtitle-2 mb-2">To</v-card-subtitle>

                  <v-text-field
                    :model-value="store.formattedResult || ''"
                    label="Result"
                    variant="outlined"
                    density="comfortable"
                    readonly
                    hide-details="auto"
                    class="mb-4"
                  >
                    <template v-slot:append-inner v-if="store.formattedResult">
                      <v-btn
                        icon="mdi-content-copy"
                        size="small"
                        variant="text"
                        @click="copyToClipboard"
                      />
                    </template>
                  </v-text-field>

                  <v-select
                    :model-value="store.toUnit"
                    @update:model-value="store.setToUnit"
                    :items="store.availableToUnits"
                    item-title="label"
                    item-value="key"
                    return-object
                    label="Select unit"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item v-bind="props">
                        <template v-slot:subtitle>
                          <span class="text-caption">{{ item.raw.description }}</span>
                        </template>
                      </v-list-item>
                    </template>
                  </v-select>
                </v-card>
              </v-col>
            </v-row>

            <!-- Conversion Formula -->
            <v-row v-if="store.result" class="mt-4">
              <v-col cols="12">
                <v-alert
                  type="info"
                  variant="tonal"
                  density="compact"
                  class="text-body-2"
                >
                  <strong>Formula:</strong> {{ store.result.formula }}
                </v-alert>
              </v-col>
            </v-row>

            <!-- Error Message -->
            <v-row v-if="store.error" class="mt-4">
              <v-col cols="12">
                <v-alert
                  type="error"
                  variant="tonal"
                  density="compact"
                  closable
                  @click:close="store.error = null"
                >
                  {{ store.error }}
                </v-alert>
              </v-col>
            </v-row>

            <!-- Action Buttons -->
            <v-row class="mt-4">
              <v-col cols="12" class="d-flex justify-center gap-2">
                <v-btn
                  color="primary"
                  variant="elevated"
                  @click="store.performConversion"
                  :disabled="!store.canPerformConversion"
                >
                  Convert
                </v-btn>
                <v-btn
                  color="secondary"
                  variant="outlined"
                  @click="store.reset"
                >
                  Reset
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Info Section -->
        <v-row class="mt-6">
          <v-col cols="12" md="6">
            <v-card elevation="2" class="pa-4">
              <v-card-title class="text-subtitle-1">
                <v-icon icon="mdi-information" class="mr-2" />
                Binary Units (IEC)
              </v-card-title>
              <v-card-text class="text-body-2">
                Binary units use base-2 (powers of 1024):
                <ul class="mt-2">
                  <li>1 KiB = 1,024 bytes</li>
                  <li>1 MiB = 1,024 KiB</li>
                  <li>1 GiB = 1,024 MiB</li>
                </ul>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card elevation="2" class="pa-4">
              <v-card-title class="text-subtitle-1">
                <v-icon icon="mdi-information" class="mr-2" />
                Decimal Units (SI)
              </v-card-title>
              <v-card-text class="text-body-2">
                Decimal units use base-10 (powers of 1000):
                <ul class="mt-2">
                  <li>1 KB = 1,000 bytes</li>
                  <li>1 MB = 1,000 KB</li>
                  <li>1 GB = 1,000 MB</li>
                </ul>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useConversionStore } from '@/stores/conversionStore'

const store = useConversionStore()

function copyToClipboard() {
  if (store.formattedResult) {
    navigator.clipboard.writeText(store.formattedResult)
  }
}
</script>

<style scoped>
.converter-main {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.gap-2 {
  gap: 0.5rem;
}
</style>
