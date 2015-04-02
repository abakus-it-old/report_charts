from openerp.addons.web.http import Controller, route, request

class ReportChartController(Controller):
    @route(['/report/chart/pie'], type='http', auth="user")
    def report_pie_chart(self,labels=None,sizes=None,colors=None,explode=None):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import cStringIO                  
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        
        if labels:
            labels = labels.split(",")
        if sizes:
            sizesTmp = sizes.split(",")
            sizes = []
            for size in sizesTmp:
                sizes.append(float(size))
        if colors:
            colors = colors.split(",")
        else:
            colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w')
        if explode:
            explodeTmp = explode.split(",")
            explode = []
            for e in explodeTmp:
                explode.append(float(e))
        
        #Demo values
        #labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        #sizes = [15, 30, 45, 10]
        #colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
        #explode = (0, 0.1, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')

        plt.pie(sizes, explode, labels, colors,autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        
        fig = plt.gcf()
        fig.patch.set_color('#FFFFFF')
        canvas = FigureCanvasAgg(fig)
        
        buf = cStringIO.StringIO()
        try:
            canvas.print_png(buf)
            data = buf.getvalue()
        finally:
            buf.close()
        
        plt.close()
        plt.clf()
        plt.cla()
        
        return request.make_response(data, headers=[('Content-Type', 'image/png')])