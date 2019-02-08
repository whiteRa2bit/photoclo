<template>
	<div>
    	<img id="imageItem" v-bind:src="imageURL" alt=""/>
	</div>
</template>

<script>
	export default {
		name: 'imageItem',
		props: ['imageURL'],
		methods: {}
	}
</script>

<style scoped>
    #imageItem {
    	height: 200px;
    	border: 2px black;
    	margin-bottom: 8px;
    	margin-top: 8px;
    	margin-left: 2px;
    	margin-right: 2px;
    }

    #imageItem:hover {
    	opacity: 0.8;
    	cursor: pointer;
    }
</style>