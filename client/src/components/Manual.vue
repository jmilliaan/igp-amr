<template>
    <div class="container">
        <div class="grid">
            <div class="arrow north-west"
                @mousedown="startCommand('1')" 
                @mouseup="stopCommand" 
                @mouseleave="stopCommand" 
                @touchend="stopCommand"></div>
            <div class="arrow north"
                @mousedown="startCommand('2')" 
                @mouseup="stopCommand" 
                @mouseleave="stopCommand" 
                @touchend="stopCommand"></div>
            <div class="arrow north-east"
                @mousedown="startCommand('3')" 
                @mouseup="stopCommand" 
                @mouseleave="stopCommand" 
                @touchend="stopCommand"></div>
            <div class="arrow west"
                @mousedown="startCommand('4')" 
                @mouseup="stopCommand" 
                @mouseleave="stopCommand" 
                @touchend="stopCommand"></div>
            <div class="stop"
                @mousedown="startCommand('5')" 
                @mouseup="stopCommand" 
                @mouseleave="stopCommand" 
                @touchend="stopCommand"></div>
            <div class="arrow east"
                @mousedown="startCommand('6')" 
                @mouseup="stopCommand" 
                @mouseleave="stopCommand" 
                @touchend="stopCommand"></div>
            <div class="arrow south-west"
                @mousedown="startCommand('7')" 
                @mouseup="stopCommand" 
                @mouseleave="stopCommand" 
                @touchend="stopCommand"></div>
            <div class="arrow south"
                @mousedown="startCommand('8')" 
                @mouseup="stopCommand" 
                @mouseleave="stopCommand" 
                @touchend="stopCommand"></div>
            <div class="arrow south-east"
                @mousedown="startCommand('9')" 
                @mouseup="stopCommand" 
                @mouseleave="stopCommand" 
                @touchend="stopCommand"></div>
        </div>
    </div>
  </template>
  
<style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
        gap: 0px;
        width: 200px;
        height: 220px;
        align-items: center;
        padding-top: 20px;
        justify-items: center;
    }

    .arrow {
        width: 0;
        height: 0;
        border-style: solid;
        margin: 0px;
    }

    .north {
    border-width: 0 20px 40px 20px;
    border-color: transparent transparent #007BFF transparent;
    }

    .stop {
        width: 40px;
        height: 40px;
        border: 10px solid red;
        background-color: red;
        border-radius: 50%;
    }

    .north-east {
    transform: rotate(45deg);
    border-width: 0 20px 40px 20px;
    border-color: transparent transparent #007BFF transparent;
    }

    .east {
    border-width: 20px 0 20px 40px;
    border-color: transparent transparent transparent #007BFF;
    }

    .south-east {
    transform: rotate(45deg);
    border-width: 20px 0 20px 40px;
    border-color: transparent transparent transparent #007BFF;
    }

    .south {
    border-width: 40px 20px 0 20px;
    border-color: #007BFF transparent transparent transparent;
    }

    .south-west {
    transform: rotate(45deg);
    border-width: 40px 20px 0 20px;
    border-color: #007BFF transparent transparent transparent;
    }

    .west {
    border-width: 20px 40px 20px 0;
    border-color: transparent #007BFF transparent transparent;
    }

    .north-west {
    transform: rotate(45deg);
    border-width: 20px 40px 20px 0;
    border-color: transparent #007BFF transparent transparent;
    }
</style>

<script>
let holdingInterval = 100; // Interval in milliseconds
let interval = null;

export default {
    name: 'ManualControl',
    props: {
        msg: String,
        ws: {
            type: Object,
            required: true
        }
    },
    methods: {
        stopCommand(){
            clearInterval(interval);
            interval= null
        },
        startCommand(number){
            this.stopCommand(); // Ensure no other intervals are running
            interval = setInterval(()=> {
                this.ws.send(number);
            }, holdingInterval);
        }
        
    }
}
</script>