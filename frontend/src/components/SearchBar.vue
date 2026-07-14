<script setup>
import { ref } from 'vue'

const props = defineProps({
  placeholder: { type: String, default: 'Search...' },
  filters: { type: Array, default: () => [] } // [{ key, label, options }]
})

const emit = defineEmits(['search', 'filter'])

const searchQuery = ref('')
const activeFilters = ref({})

// Initialize filter values
props.filters.forEach(f => {
  activeFilters.value[f.key] = f.options?.[0] || 'All'
})

const onSearch = () => {
  emit('search', searchQuery.value)
}

const onFilter = () => {
  emit('filter', { ...activeFilters.value })
}
</script>

<template>
  <div class="tma-search">
    <div class="row g-2 align-items-center">
      <div class="col-12" :class="filters.length > 0 ? 'col-md-6' : ''">
        <div class="search-input-wrapper">
          <i class="bi bi-search search-icon"></i>
          <input
            type="text"
            class="search-input"
            :placeholder="placeholder"
            v-model="searchQuery"
            @input="onSearch"
          />
        </div>
      </div>
      <div
        v-for="filter in filters"
        :key="filter.key"
        class="col-6"
        :class="`col-md-${Math.floor(6 / filters.length)}`"
      >
        <select
          class="form-select form-select-sm"
          v-model="activeFilters[filter.key]"
          @change="onFilter"
          style="font-size: 0.85rem; border: 1.5px solid #e2e8f0; border-radius: 8px;"
        >
          <option v-for="opt in filter.options" :key="opt" :value="opt">
            {{ filter.label }}: {{ opt }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>
