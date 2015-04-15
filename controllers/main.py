from openerp.addons.web.http import Controller, route, request

class ReportChartController(Controller):
    @route(['/report/chart/pie'], type='http', auth="user")
    def report_pie_chart(self,labels=None,sizes=None,colors=None,explode=None):
        import matplotlib
        matplotlib.use('Agg')
        matplotlib.rcParams['font.size'] = 14
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
        
        plt.figure(figsize=(8,4))
        plt.pie(sizes, explode, labels, colors,autopct='%1.1f%%', shadow=False, startangle=90)
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
        
        plt.close('all')
        plt.clf()
        plt.cla()
        
        return request.make_response(data, headers=[('Content-Type', 'image/png')])
