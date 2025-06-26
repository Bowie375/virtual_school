<template>
    <div class="image-carousel">
      <div class="carousel-slide">
        <img :src="images[currentIndex].src" :alt="images[currentIndex].alt" />
      </div>
      <div class="carousel-indicators">
        <span v-for="(image, index) in images" :key="index" :class="{ active: currentIndex === index }" @click="goToSlide(index)"></span>
      </div>
    </div>
  </template>
  
  <script setup>
    import { ref, defineProps } from 'vue'

    // 定义 props
    const props = defineProps({
    spotName: {
        type: String,
        required: true
    }
    })

    // 响应式状态
    const currentIndex = ref(0)

    // 动态生成图片数组
    const imagess = import.meta.glob('/src/assets/*.jpg', { eager: true })
    const images = []
    let i = 1

    while(true) {
        console.log(i)
        const path = `/src/assets/${props.spotName}${i}.jpg`
        console.log(path)
        if(!imagess[path]?.default) break
        
        images.push({
            src: `/src/assets/${props.spotName}${i}.jpg`,
            alt: `Image ${i}`
            })
        i++
    }
    console.log(images)

    // 切换方法
    const goToSlide = (index) => {
        currentIndex.value = index
    }
  </script>
  
  <style scoped>

.image-carousel {
  /* 外层容器设置固定尺寸 */
  width: 100%;
  height: 700px;
  position: relative;
  overflow: hidden;
}

.carousel-slide {
  /* 滑动项设置 */
  width: 100%;
  height: 100%; /* 继承外层容器高度 */
  flex-shrink: 0;
  position: relative; /* 新增定位上下文 */
}

.carousel-slide img {
  /* 图片绝对定位填充 */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  object-fit: cover; 
  
  /* 保证最小尺寸填充 */
  min-width: 100%;
  min-height: 100%;
  
  /* 处理极小图片 */
  image-rendering: -webkit-optimize-contrast;
}
  .carousel-indicators {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
  }
  .carousel-indicators span {
    cursor: pointer;
    display: inline-block;
    width: 10px;
    height: 10px;
    margin: 0 5px;
    background-color: #ccc;
    border-radius: 50%;
  }
  .carousel-indicators span.active {
    background-color: #333;
  }
  </style>