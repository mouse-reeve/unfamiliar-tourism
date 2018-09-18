var black;
var white;

function setup() {
    randomSeed(seed);

    var container = document.getElementById('skyline');
    var canvas = createCanvas(1000, 500);
    canvas.parent(container);

    black = color(0);
    white = color(255);
    // this is important
    colorMode(HSL, 100);

    // the gradient is too complex to re-render
    if ('sky' in skyline_data) {
        draw_from_data(skyline_data.sky);
    } else {
        noLoop();
    }
    var end_time = new Date();
}

function draw() {
    var start_time = new Date();
    if (skyline_data.mountains) {
        draw_from_data(skyline_data.mountains);
    }
    draw_from_data(skyline_data.foreground);
    if ('buildings' in skyline_data) {
        draw_from_data(skyline_data.reflection);
        draw_from_data(skyline_data.buildings);
    }
    var end_time = new Date();
}

var createColor = function (color_data) {
    return color(color_data.as_string);
}

var draw_from_data = function(image_data) {
    if (!image_data) return;

    if (Array.isArray(image_data)) {
        for (var i = 0; i < image_data.length; i++) {
            draw_from_data(image_data[i]);
        }
    }

    if ('points' in image_data) {
        for (var i = 0; i < image_data.points.length; i++) {
            var item = image_data.points[i];
            push();
            stroke(createColor(item.color));
            point(item.x, item.y);
            pop();
        }
    }

    if ('rects' in image_data) {
        for (var i = 0; i < image_data.rects.length; i++) {
            var item = image_data.rects[i];
            push();
            noStroke();
            fill(createColor(item.color));
            rect(item.x, item.y, item.w, item.h);
            pop();
        }
    }

    if ('shapes' in image_data) {
        for (var i = 0; i < image_data.shapes.length; i++) {
            var item = image_data.shapes[i];
            push();
            noStroke();
            fill(createColor(item.color));
            beginShape();
            for (var v = 0; v < item.vertices.length; v++) {
                var vert = item.vertices[v];
                var offsets = [vert[2] || 0, vert[3] || 0];
                for (var j = 0; j < offsets.length; j++) {
                    if (!offsets[j]) continue;

                    if (vert.current_offset === undefined) {
                        vert.current_offset = random(-1, 1);
                        vert.direction = random(-1, 1);
                    }
                    if (Math.abs(vert.current_offset + vert.direction) > offsets[j]) {
                        vert.direction *= -1;
                    }
                    vert.current_offset += vert.direction;
                    offsets[j] = vert.current_offset;
                }
                vertex(vert[0] + offsets[0], vert[1] + offsets[1]);
            }
            if (item.contour !== undefined) {
                beginContour();
                for (var v = 0; v < item.contour.length; v++) {
                    vertex(item.contour[v][0], item.contour[v][1]);
                }
                endContour();
            }
            endShape(CLOSE);
            pop();
        }
    }
};
