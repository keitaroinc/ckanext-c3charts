this.ckan = this.ckan || {};
this.ckan.views = this.ckan.views || {};
this.ckan.views.c3charts = this.ckan.views.c3charts || {};

(function (self, $) {
    "use strict";
    var api = {
        get: function (action, params) {
            var api_ver = 3;
            var base_url = ckan.sandbox().client.endpoint;
            params = $.param(params);
            var url = base_url + '/api/' + api_ver + '/action/' + action + '?' + params;
            return $.getJSON(url);
        },
        post: function (action, data) {
            var api_ver = 3;
            var base_url = ckan.sandbox().client.endpoint;
            var url = base_url + '/api/' + api_ver + '/action/' + action;
            return $.post(url, JSON.stringify(data), "json");
        }
    };
    self.init = function init(elementId, resource, resourceView) {
        initPlot(elementId, resource, resourceView);
    };

    function initPlot(elementId, resource, resourceView) {

        var queryParams = generateQueryParams(resource, {});
        // If SQL Statement is available for the resource view
        // use that to fetch data for the charts otherwise
        // fetch the entire resource data
        // TODO: Refactor & optimize
        if (resourceView.sql_expression) {
            if (resourceView.key_fields) {
                if (resourceView.chart_type == 'Table Chart' ||
                    resourceView.chart_type == 'Simple Chart') {
                    textChartBuilder(elementId, resourceView, resourceView.sql_data);
                } else {
                    c3.generate(chartBuilder(elementId, resourceView, resourceView.sql_data));
                }
            } else {
                $(elementId).append("No keys defined");
            }

        } else {
            $.when(
                recline.Backend.Ckan.fetch(resource),
                recline.Backend.Ckan.query(queryParams, resource)
            ).done(function (fetch, query) {
                var fields = fetch.fields,
                    data = query.hits;
                if (resourceView.key_fields) {
                    if (resourceView.chart_type == 'Table Chart' ||
                        resourceView.chart_type == 'Simple Chart') {
                        textChartBuilder(elementId, resourceView, data);
                    } else {
                        c3.generate(chartBuilder(elementId, resourceView, data));
                    }
                } else {
                    $(elementId).append("No keys defined");
                }
            });
        }
    }

    function chartBuilder(elementId, resourceView, data) {
        var i, j,
            chart_type = resourceView.chart_type,
            x_list = [],
            key_fields = resourceView.key_fields,
            x_fields = resourceView.x_fields,
            legend = (resourceView.legend == 'hide') ? {show: false} : {
                position: resourceView.legend,
                item: {
                    onclick: function (id) {
                    }
                }
            };

        var labelX = resourceView.measure_unit_x;
        var labelY = resourceView.measure_unit_y;
        var positionX = resourceView.x_label_position;
        var positionY = resourceView.y_label_position;

        switch (chart_type) {
            case 'Pie Chart':
                chart_type = 'pie';
                break;
            case 'Donut Chart':
                chart_type = 'donut';
                break;
            case 'Bar Chart':
                chart_type = 'bar';
                break;
            case 'Stacked Bar Chart':
                chart_type = 'bar';
                break;
            case 'Line Chart':
                chart_type = 'line';
                break;
            case 'Area-spline Chart':
                chart_type = 'area-spline';
                break;
            case 'Spline Chart':
                chart_type = 'spline';
                break;
        }

        if (!Array.isArray(key_fields)) {
            key_fields = [key_fields];
        }

        if (resourceView.aggregate) {
            var remap_data = [],
                data_len, remap_data_len, aggregator, flag, tmp;
            for (i = 0, data_len = data.length; i < data_len; i++) {
                aggregator = data[i][x_fields];
                flag = false;
                for (j = 0, remap_data_len = remap_data.length; j < remap_data_len; j++) {
                    if (remap_data[j][x_fields] === aggregator) {
                        tmp = parseFloat(data[i][key_fields]);
                        if (!isNaN(tmp)) {
                            remap_data[j][key_fields] += tmp;
                        }
                        flag = true;
                        break;
                    }
                }
                if (!flag) {
                    tmp = parseFloat(data[i][key_fields]);
                    if (!isNaN(tmp)) {
                        data[i][key_fields] = tmp;
                        remap_data.push(data[i]);
                    }
                }
            }
            data = remap_data;
            data.sort(function (a, b) {
                return parseFloat(a[x_fields]) - parseFloat(b[x_fields]);
            })
        }

        if (Array.isArray(x_fields)) {
            for (i = 0; i < data.length; i++) {
                for (j = 0; j < x_fields.length; j++) {
                    if (!x_list[i]) {
                        x_list[i] = data[i][x_fields[j]];
                    } else {
                        x_list[i] += '-' + data[i][x_fields[j]];
                    }
                }
            }
        } else {
            for (i in data) {
                x_list.push(data[i][x_fields]);
            }
        }

        if (resourceView.remap_key != '') {
            remap_data = [];
            var remap_key_fields = [],
                tmp_object = {},
                remap_field = resourceView.remap_key;
            for (i in data) {
                tmp_object[data[i][remap_field]] = data[i][key_fields];
                remap_data.push(tmp_object);
                remap_key_fields.push(data[i][remap_field]);
            }
            data = remap_data;
            key_fields = remap_key_fields;
        }

        var chartContainer = $(elementId).parent();
        var width = chartContainer.attr('data-graph_width');
        var height = chartContainer.attr('data-graph_height');
        var showAxis = chartContainer.attr('data-show_axis');

        if (typeof showAxis === 'undefined') {
            showAxis = true;
        } else {
            if (showAxis === '1') {
                showAxis = true;
            } else if (showAxis === '0') {
                showAxis = false;
            } else {
                showAxis = true;
            }
        }

        var colorPattern = ['#00A58D', '#09505D', '#00587C', '#00A6BC', '#9FCD91', '#293A4C', '#83CCD8', '#A0C1C2'];
        if (resourceView.sql_expression) {
            data = resourceView.sql_data;
            if (resourceView.use_sql_keys)
                key_fields = resourceView.sql_keys;
        }
        var x_tick = {
            culling: false,
            fit: true,
            centered: true,
            format: function (d) {
                var measureUnit = resourceView.measure_unit_x;
                if (measureUnit) return x_list[d];
                return x_list[d];
            }
        };
        var y_tick = {
            format: function (x) {
                return parseInt(x)
            }
        };

        if (resourceView.x_tick_count)
            x_tick['count'] = resourceView.x_tick_count;

        if (resourceView.y_tick_count)
            y_tick['count'] = resourceView.y_tick_count;

        var r_pad, l_pad, t_pad, b_pad;
        if (resourceView.r_padding)
            r_pad = resourceView.r_padding;
        if (resourceView.l_padding)
            l_pad = resourceView.l_padding;
        if (resourceView.t_padding)
            t_pad = resourceView.t_padding;
        if (resourceView.b_padding)
            b_pad = resourceView.b_padding;

        return {
            size: {
                width: Number(width),
                height: Number(height)
            },
            bindto: elementId,
            data: {
                json: data,
                keys: {
                    value: key_fields
                },
                type: chart_type,
                groups: resourceView.chart_type != 'Stacked Bar Chart' || [key_fields],
                labels: {
                    format: function (value) {
                        return value;
                    }
                }
            },
            padding: {
                top: parseInt(t_pad),
                bottom: parseInt(b_pad),
                right: parseInt(r_pad),
                left: parseInt(l_pad)
            },
            axis: {
                x: {
                    type: 'category',
                    categories: x_list,
                    tick: x_tick,
                    label: {
                        text: labelX,
                        position: positionX
                    },
                    show: showAxis
                },
                y: {
                    tick: y_tick,
                    label: {
                        text: labelY,
                        position: positionY
                    },
                    show: showAxis
                },
                rotated: !!resourceView.rotated
            },
            color: {
                pattern: colorPattern
            },
            grid: {
                x: {
                    show: !!resourceView.x_grid
                },
                y: {
                    show: !!resourceView.y_grid
                }
            },
            legend: legend
        }
    }


    function textChartBuilder(elementId, resourceView, data) {

        function buildTable(resourceView, data) {
            var rowheaders = $('<tr />'),
                rowdata = $('<tr />'),
                datalength = data.length,
                i = datalength - 4;

            for (i; i < datalength; i++) {
                rowheaders.append(
                    $('<td />')
                        .text(data[i][resourceView.x_fields])
                );
                rowdata.append(
                    $('<td />')
                        .text(data[i][resourceView.key_fields])
                )
            }

            return $('<table />')
                .addClass('table')
                .addClass('table-bordered')
                .addClass('table-striped')
                .addClass('chart-table')
                .append(
                    $('<thead />')
                        .append(
                            $('<tr />')
                                .append(
                                    $('<th colspan="4" \>')
                                        .text(resourceView.key_fields)
                                )
                        )
                )
                .append(
                    $('<tbody />')
                        .append(rowheaders)
                        .append(rowdata)
                );
        }

        var keyField = resourceView.key_fields,
            tableNumber = 0,
            datalength = data.length,
            i = datalength - 4,
            measureUnit = resourceView.measure_unit,
            header = resourceView.header,
            triangle;

        switch (resourceView['text_chart_number_action']) {
            case 'average':
                for (i = 0; i < datalength; i++) {
                    tableNumber += Number(data[i][keyField]);
                }
                tableNumber = Math.round((tableNumber / datalength) * 100) / 100;
                break;
            case 'substract':
                tableNumber = data[datalength - 1][keyField] - data[datalength - 2][keyField];
                tableNumber = Math.round(tableNumber * 100) / 100;
                if (tableNumber > 0) {
                    triangle = $('<img src="/triangle-up.png" width="45px" style="padding-left: 24px; padding-bottom:35px" />');
                } else if (tableNumber < 0) {
                    triangle = $('<img src="/triangle-down.png" width="45px" style="padding-left: 24px; padding-bottom:0px" />')
                } else {
                    triangle = $('<div />');
                }
                break;
            case 'last':
                tableNumber = data[datalength - 1][keyField];
                break;
        }

        if (!header) {
            header = keyField;
        }

        if (measureUnit) {
            tableNumber = tableNumber + measureUnit;
        }

        var textChart = $('<div class="textChart" />')
            .append(
                $('<div />')
                    .addClass('text-center')
                    .addClass('table-number')
                    .text(tableNumber)
                    .append(triangle)
            );


        if (resourceView.chart_type == 'Table Chart') {
            textChart.append(buildTable(resourceView, data));
        }

        $(elementId)
            .addClass('c3chart')
            .append(textChart);
    }

    function generateQueryParams(resource, params) {
        var query = {
            filters: [],
            sort: [],
            size: 500
        };
        return query;
    }

})(this.ckan.views.c3charts, this.jQuery, this._);