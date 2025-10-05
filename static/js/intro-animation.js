import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"
;(async () => {
  const VISITED_KEY = "exoplanet_visited"

  function initIntroAnimation() {
    try {
      // Check if user has visited before
      const hasVisited = localStorage.getItem(VISITED_KEY)

      if (hasVisited) {
        return // Skip animation
      }

      const introDiv = document.getElementById("intro-animation")
      const canvas = document.getElementById("intro-canvas")

      if (!introDiv || !canvas) {
        console.error("[v0] Animation elements not found")
        return
      }

      // Show animation container
      introDiv.classList.add("active")

      // Create scene
      const scene = new THREE.Scene()
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)

      const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: true,
        alpha: true,
      })

      renderer.setSize(window.innerWidth, window.innerHeight)
      renderer.setClearColor(0x000000, 1)

      // Create stars
      const starsGeometry = new THREE.BufferGeometry()
      const starVertices = []

      for (let i = 0; i < 2000; i++) {
        const x = (Math.random() - 0.5) * 2000
        const y = (Math.random() - 0.5) * 2000
        const z = (Math.random() - 0.5) * 2000
        starVertices.push(x, y, z)
      }

      starsGeometry.setAttribute("position", new THREE.Float32BufferAttribute(starVertices, 3))

      const starsMaterial = new THREE.PointsMaterial({
        color: 0xffffff,
        size: 2,
        transparent: true,
        opacity: 0.8,
      })

      const stars = new THREE.Points(starsGeometry, starsMaterial)
      scene.add(stars)

      // Create central planet
      const planetGeometry = new THREE.SphereGeometry(5, 32, 32)
      const planetMaterial = new THREE.MeshPhongMaterial({
        color: 0x667eea,
        emissive: 0x112244,
        shininess: 30,
      })
      const planet = new THREE.Mesh(planetGeometry, planetMaterial)
      scene.add(planet)

      // Create data nodes around planet
      const nodes = []
      const nodePositions = [
        { x: -15, y: 12, z: 0, color: 0x4facfe },
        { x: 15, y: 12, z: 0, color: 0x43e97b },
        { x: -15, y: -12, z: 0, color: 0xf093fb },
        { x: 15, y: -12, z: 0, color: 0xfa709a },
      ]

      nodePositions.forEach((pos) => {
        const nodeGeometry = new THREE.BoxGeometry(3, 3, 3)
        const nodeMaterial = new THREE.MeshPhongMaterial({
          color: pos.color,
          emissive: pos.color,
          emissiveIntensity: 0.3,
        })
        const node = new THREE.Mesh(nodeGeometry, nodeMaterial)
        node.position.set(pos.x, pos.y, pos.z)
        scene.add(node)
        nodes.push(node)
      })

      // Add lights
      const ambientLight = new THREE.AmbientLight(0x404040, 2)
      scene.add(ambientLight)

      const pointLight = new THREE.PointLight(0xffffff, 2, 100)
      pointLight.position.set(10, 10, 10)
      scene.add(pointLight)

      camera.position.z = 40
      camera.position.y = 5

      let time = 0
      let animationId

      // Animation loop
      function animate() {
        animationId = requestAnimationFrame(animate)
        time += 0.01

        // Rotate stars
        stars.rotation.y += 0.0002

        // Rotate planet
        planet.rotation.y += 0.005

        // Animate nodes
        nodes.forEach((node, i) => {
          node.rotation.y += 0.01
          node.position.y += Math.sin(time * 2 + i) * 0.02
        })

        // Camera movement
        camera.position.x = Math.sin(time * 0.1) * 8
        camera.lookAt(0, 0, 0)

        renderer.render(scene, camera)
      }

      animate()

      // Handle window resize
      function onResize() {
        camera.aspect = window.innerWidth / window.innerHeight
        camera.updateProjectionMatrix()
        renderer.setSize(window.innerWidth, window.innerHeight)
      }
      window.addEventListener("resize", onResize)

      // End animation after 4 seconds
      setTimeout(() => {
        introDiv.classList.add("fade-out")
        localStorage.setItem(VISITED_KEY, "true")

        setTimeout(() => {
          introDiv.classList.remove("active")
          cancelAnimationFrame(animationId)
          window.removeEventListener("resize", onResize)

          // Clean up Three.js resources
          renderer.dispose()
          starsGeometry.dispose()
          starsMaterial.dispose()
          planetGeometry.dispose()
          planetMaterial.dispose()
          nodes.forEach((node) => {
            node.geometry.dispose()
            node.material.dispose()
          })
        }, 1000)
      }, 4000)
    } catch (error) {
      console.error("[v0] Animation error:", error)
      const introDiv = document.getElementById("intro-animation")
      if (introDiv) {
        introDiv.classList.remove("active")
      }
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initIntroAnimation)
  } else {
    initIntroAnimation()
  }
})()
