class IShader:
    def __init__(self, model, light_dir):
        self.model = model
        self.light_dir = light_dir
        self.varying_intensity = None

    def vertex(self, iface, nthvert):
        gl_vertex = self.model.vert(iface, nthvert)
        gl_vertex = self.viewport_projection(gl_vertex)
        self.varying_intensity[nthvert] = max(0.0, self.model.normal(iface, nthvert) * self.light_dir)
        return gl_vertex

    def fragment(self, bar, color):
        intensity = sum(i * bar[j] for j, i in enumerate(self.varying_intensity))
        color.r = color.g = color.b = int(255 * intensity)
        return False  # No need to discard the pixel

    def viewport_projection(self, vertex):
        gl_vertex = self.viewport_matrix @ self.projection_matrix @ self.model_view_matrix @ vertex
        return gl_vertex