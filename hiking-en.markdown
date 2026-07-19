---
layout: page
title: Hiking
lang: en
lang_ref: hiking
permalink: /hiking/en/
---

<h1>Hiking</h1>

{% for route in site.data.hiking.routes %}
<h2>
{{ route.heading_en }}
</h2>
<strong>
  {%- for place in route.places -%}
    {{ place.name }}
    {% unless forloop.last %}
      {%- assign next_index = forloop.index0 | plus: 1 -%}
      {%- assign next_place = route.places[next_index] -%}
      <a href="#{{ place.name | slugify }}-{{ next_place.name | slugify }}">➔</a>
    {% endunless %}
  {%- endfor -%}
</strong>
({{ route.length }} km)
<p>{{ route.description_en }}</p>
{% capture full_geojson_path %}/assets/maps/{{ route.map_filename }}.geojson{% endcapture %}
{% include vector_map.html id=route.map_filename file=full_geojson_path color="#0080ff" height="300px" %}
{% endfor %}

---

{% for item in site.data.hiking.hikes %}
<h3> {{ item.from }} → {{ item.to }} ({{ item.date }}, {{ item.length }}km, ↑ {{ item.elevation_gain }}m, ↓ {{ item.elevation_loss }}m)
<a id="{{ item.from | slugify }}-{{ item.to | slugify }}"></a>
<span class="map-trigger" data-trail-path="/assets/maps/map_{{ item.from | slugify }}_{{ item.to | slugify }}.geojson">🗺️</span>
</h3>

<!-- 1. The Main Grid Container -->
<div class="dynamic-gallery">
  {% for image in item.images %}
    {% assign rows = image.row_span | default: 1 %}
    {% assign cols = image.col_span | default: 1 %}

    <div class="gallery-item span-cols-{{ cols }} span-rows-{{ rows }}">
      <a href="{{ image.click_url }}" target="_blank" rel="noopener" class="image-link">
        <img src="{{ image.image_url }}" alt="Hiking photo">
      </a>
      <div class="gallery-caption">
        {{ image.description_en }}
      </div>
    </div>
  {% endfor %}
</div>

{% endfor %}


<!-- Alignment Script -->
<script>
  document.addEventListener("DOMContentLoaded", function () {
    const galleryItems = document.querySelectorAll(".gallery-item");

    // Create a ResizeObserver to monitor caption heights dynamically
    const resizeObserver = new ResizeObserver((entries) => {
      for (let entry of entries) {
        const item = entry.target;

        const caption = item.querySelector(".gallery-caption");
        if (caption) {
          // Measure the exact pixel height of the text wrapper
          const captionHeight = caption.getBoundingClientRect().height;

          // Apply that exact height as a bottom margin to push down elements directly below it
          item.style.marginBottom = `${captionHeight}px`;
        }
      }
    });

    // Observe each gallery item
    galleryItems.forEach((item) => resizeObserver.observe(item));
  });
</script>
