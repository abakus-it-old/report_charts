from openerp.addons.web.http import Controller, route, request

class ReportChartController(Controller):
    @route(['/report/chart/pie'], type='http', auth="user")
    def report_pie_chart(self,labels=None,sizes=None,colors=None,explode=None):
        import matplotlib
        matplotlib.use('Agg')
        matplotlib.rcParams['font.size'] = 14
        import matplotlib.pyplot as plt
        plt.rcParams['patch.edgecolor'] = '#EE7F2E' 
        plt.rcParams['patch.linewidth'] = 2  

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
            #colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w')
            #custom colours
            colors = ('#A6A6A6','#F6F3F3','#A5A085','#B0BFBF','#E9EAEE')
        if explode:
            explodeTmp = explode.split(",")
            explode = []
            for e in explodeTmp:
                explode.append(float(e))
        
        fig = plt.figure(figsize=(6,4))
        fig.patch.set_color('#FFFFFF')
        ax = fig.add_subplot(111)
        ax.pie(sizes, explode, labels, colors,autopct='%1.1f%%', shadow=False, startangle=90)
        ax.axis('equal')

        canvas = FigureCanvasAgg(fig)
        
        buf = cStringIO.StringIO()
        try:
            canvas.print_png(buf)
            data = buf.getvalue()
        finally:
            buf.close()
        
        return request.make_response(data, headers=[('Content-Type', 'image/png')])
