<script setup>
import { defineProps, defineEmits, onMounted, onBeforeUnmount, ref } from 'vue'
import { Modal } from 'bootstrap'

const props = defineProps({
  id: { type: String, required: true },
  title: { type: String, default: 'Confirm Action' },
  message: { type: String, default: 'Are you sure you want to proceed?' },
  confirmText: { type: String, default: 'Confirm' },
  confirmClass: { type: String, default: 'btn-danger' }
})

const emit = defineEmits(['confirm', 'cancel'])

let modalInstance = null

onMounted(() => {
  const el = document.getElementById(props.id)
  if (el) {
    modalInstance = new Modal(el)
    el.addEventListener('hidden.bs.modal', () => emit('cancel'))
  }
})

onBeforeUnmount(() => {
  if (modalInstance) modalInstance.dispose()
})

const handleConfirm = () => {
  emit('confirm')
  if (modalInstance) modalInstance.hide()
}
</script>

<template>
  <div class="modal fade" :id="id" tabindex="-1" :aria-labelledby="`${id}Label`" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" :id="`${id}Label`">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ title }}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p class="mb-0" style="font-size: 0.95rem; color: #4a5568;">{{ message }}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-sm" :class="confirmClass" @click="handleConfirm">
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
