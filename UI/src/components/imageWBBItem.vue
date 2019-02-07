<template>
	<div>
    	<img id="imageWBBItem" v-bind:src="image.url" alt=""/>
	</div>
</template>

<script>
	export default {
		name: 'imageWBBItem',
		props: ['image'],
		methods: {}
	}
</script>

<style scoped>
    #imageWBBItem {
        margin: auto;
        overflow: auto;
        display: block;
    }
</style>