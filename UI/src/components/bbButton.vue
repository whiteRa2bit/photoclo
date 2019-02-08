<template>
	<button class="mybbButton" />
</template>

<script>

	export default {
		name: 'bbButton',
		props: [],
        watch: {},
		methods: {},
	}
</script>

<style scoped>
    .mybbButton {
        border: 2px solid rgba(255, 255, 0, 0.5) !important;
    }

    .mybbButton:hover {
        border: 3px solid rgba(255, 255, 0, 1) !important;
    }
</style>