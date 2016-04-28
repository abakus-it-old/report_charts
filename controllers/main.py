from openerp.addons.web.http import Controller, route, request
import numpy as np
import logging
_logger = logging.getLogger(__name__)

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
        
        def my_autopct(pct):
            total=sum(sizes)
            val=int(pct*total/100.0)
            return '{p:.2f}% ({v:d})'.format(p=pct,v=val)

        fig = plt.figure(figsize=(7,4))
        fig.patch.set_color('#FFFFFF')
        ax = fig.add_subplot(111)
        patches = ax.pie(sizes, explode, labels, colors, shadow=False, startangle=90, radius=1.2) #autopct='%1.1f%%'
        ax.axis('equal')

        # Legend
        values = np.array(sizes)
        porcent = 100.*values/values.sum()
        labels_with_porcents = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, porcent)]
        ax.legend(labels_with_porcents, loc='best', bbox_to_anchor=(0.5, 0.7), fontsize=12)

        canvas = FigureCanvasAgg(fig)
        
        buf = cStringIO.StringIO()
        try:
            canvas.print_png(buf)
            data = buf.getvalue()
        finally:
            buf.close()
        
        return request.make_response(data, headers=[('Content-Type', 'image/png')])
