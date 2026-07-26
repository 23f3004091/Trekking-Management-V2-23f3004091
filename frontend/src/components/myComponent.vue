<script setup>
import { defineProps } from 'vue';

defineProps({
    username: {type: String, required : true, default : "GyanPrakashash"}
})

</script>

<template>
    <div>
        <h1>
            my name is {{ username }}
        </h1>
    </div>
</template>