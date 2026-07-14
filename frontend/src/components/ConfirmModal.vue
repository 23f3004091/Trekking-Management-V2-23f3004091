<script setup>
import { watch, nextTick } from 'vue'

const props = defineProps({
  id: { type: String, required: true },
  title: { type: String, default: 'Confirm Action' },
  message: { type: String, default: 'Are you sure you want to proceed?' },
  confirmText: { type: String, default: 'Confirm' },
  confirmClass: { type: String, default: 'btn-danger' },
  modelValue: { type: Boolean, default: false }
})

const emit = defineEmits(['confirm', 'cancel', 'update:modelValue'])

const close = () => {
  emit('update:modelValue', false)
  emit('cancel')
}

const handleConfirm = () => {
  emit('confirm')
  emit('update:modelValue', false)
}

// Prevent body scroll when modal is open
watch(() => props.modelValue, (val) => {
  nextTick(() => {
    if (val) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
  })
})
</script>

<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div
        v-if="modelValue"
        class="confirm-modal-overlay"
        :id="`${id}-overlay`"
        @click.self="close"
        role="dialog"
        :aria-labelledby="`${id}Label`"
        aria-modal="true"
      >
        <div class="confirm-modal-box">
          <div class="confirm-modal-header">
            <h5 class="confirm-modal-title" :id="`${id}Label`">
              <i class="bi bi-exclamation-triangle-fill me-2 text-warning"></i>{{ title }}
            </h5>
            <button type="button" class="confirm-modal-close" @click="close" aria-label="Close">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>
          <div class="confirm-modal-body">
            <p class="mb-0">{{ message }}</p>
          </div>
          <div class="confirm-modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" @click="close">Cancel</button>
            <button type="button" class="btn btn-sm" :class="confirmClass" @click="handleConfirm">
              {{ confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.confirm-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1055;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.confirm-modal-box {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 480px;
  overflow: hidden;
}

.confirm-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e9ecef;
}

.confirm-modal-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: #1a1a2e;
}

.confirm-modal-close {
  background: none;
  border: none;
  font-size: 1rem;
  color: #6c757d;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
  transition: color 0.2s;
}
.confirm-modal-close:hover {
  color: #1a1a2e;
}

.confirm-modal-body {
  padding: 1.25rem;
  font-size: 0.95rem;
  color: #4a5568;
}

.confirm-modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

/* Transition animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-active .confirm-modal-box,
.modal-fade-leave-active .confirm-modal-box {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-from .confirm-modal-box,
.modal-fade-leave-to .confirm-modal-box {
  transform: scale(0.95) translateY(-10px);
  opacity: 0;
}
</style>
