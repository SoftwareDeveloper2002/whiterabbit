class Navbar:
    def render(self):
        return """
        <nav class="fixed w-full bg-white shadow z-50">
            <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                <h1 class="text-2xl font-bold text-red-700">WhiteRabbit</h1>
                <div class="space-x-6">
                    <a href="#home" class="text-gray-700 hover:text-red-600 font-medium">Home</a>
                    <a href="#features" class="text-gray-700 hover:text-red-600 font-medium">Features</a>
                    <a href="#quickstart" class="text-gray-700 hover:text-red-600 font-medium">Quick Start</a>
                    <a href="#docs" class="text-gray-700 hover:text-red-600 font-medium">Docs</a>
                </div>
            </div>
        </nav>
        """
