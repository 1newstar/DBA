$(document).ready(function(){
            var canvas = document.getElementById('canvas');
            var stage = new JTopo.Stage(canvas);
            var scene = new JTopo.Scene(stage);
            scene.background="./img/back/03.png";
            scene.alpha = 1;

            //显示工具栏
            showJTopoToobar(stage);

            //新建节点
            function addNode(hostname,ip,type){
                var node = new JTopo.Node(hostname);
                node.setImage('./img/test/'+ type +'.png', true);
                node.font="12px Consolas";
                node.fontColor="#CCCC";
                scene.add(node);

                node.mouseover(function(){
                    this.text = ip;
                });
                node.mouseout(function(){
                    this.text = hostname;
                });
                return node;
            }

            //新建连接
            function addLink(nodeA, nodeZ){
                var link = new JTopo.FlexionalLink(nodeA, nodeZ);
                link.strokeColor = '204,204,204';
                link.lineWidth = 1;
                scene.add(link);
                return link;
            }

            // 手动连线
            function autoaddLink() {
                var beginNode = null;
                var tempNodeA = new JTopo.Node('tempA');
                tempNodeA.setSize(1, 1);
                var tempNodeZ = new JTopo.Node('tempZ');
                tempNodeZ.setSize(1, 1);
                var link = new JTopo.FlexionalLink(tempNodeA, tempNodeZ);
                link.strokeColor = '204,204,204';
                link.lineWidth = 1;


                //监听鼠标双击松开事件
                scene.dbclick(function(e){
                    if(e.button == 2){
                        scene.remove(link);
                        return;
                    }
                    if(e.target != null && e.target instanceof JTopo.Node){
                        if(beginNode == null){
                            beginNode = e.target;
                            scene.add(link);
                            tempNodeA.setLocation(e.x, e.y);
                            tempNodeZ.setLocation(e.x, e.y);
                        }else if(beginNode !== e.target){
                            var endNode = e.target;
                            //var l = new JTopo.FlexionalLink(beginNode, endNode);
                            //l.strokeColor = '204,204,204';
                            //l.lineWidth = 1;
                            //scene.add(l);
                            var l = addLink(beginNode, endNode);
                            beginNode = null;
                            scene.remove(link);
                        }else{
                            beginNode = null;
                                }
                            }else{
                                scene.remove(link);
                            }
                        });

                //监听鼠标按下事件
                scene.mousedown(function(e){
                    if(e.target == null || e.target === beginNode || e.target === link){
                        scene.remove(link);
                        }
                });


                //监听鼠标移动事件
                scene.mousemove(function(e){
                    tempNodeZ.setLocation(e.x, e.y);
                });
            }

        var nodes = [{'ip': '106.1.2.1', 'hostname': 'slb01', 'type': 'SLB'}, {'ip': '106.1.2.2', 'hostname': 'slb02', 'type': 'SLB'}, {'ip': '192.168.1.5', 'hostname': 'app02', 'type': 'ECS'}, {'ip': '', 'hostname': 'client', 'type': 'internat'}, {'ip': '192.168.1.3', 'hostname': 'web03', 'type': 'ECS'}, {'ip': '192.168.1.2', 'hostname': 'web02', 'type': 'ECS'}, {'ip': '192.168.1.1', 'hostname': 'web01', 'type': 'ECS'}, {'ip': '192.168.2.2', 'hostname': 'db02', 'type': 'RDS'}, {'ip': '192.168.2.1', 'hostname': 'db01', 'type': 'RDS'}, {'ip': '192.168.1.4', 'hostname': 'app01', 'type': 'ECS'},{'ip': '192.168.10.1', 'hostname': 'tomcat01', 'type': 'ECS'},{'ip': '192.168.10.2', 'hostname': 'tomcat02', 'type': 'ECS'},{'ip': '192.168.2.3', 'hostname': 'db03', 'type': 'RDS'}];
        var links = [{'source': 'client', 'destination': 'slb02'}, {'source': 'web03', 'destination': 'db01'}, {'source': 'slb01', 'destination': 'web02'}, {'source': 'web02', 'destination': 'db01'}, {'source': 'web01', 'destination': 'db01'}, {'source': 'app02', 'destination': 'db02'}, {'source': 'slb01', 'destination': 'web01'}, {'source': 'client', 'destination': 'slb01'}, {'source': 'slb02', 'destination': 'app02'}, {'source': 'slb01', 'destination': 'web03'}, {'source': 'app01', 'destination': 'db02'}, {'source': 'slb02', 'destination': 'app01'}];


        //$.ajax({
        //        type: 'post',
        //        dataType: 'josn',
        //        url: 'rul地址',
        //        data: '参数',
        //        success: function (data) {
        //            alert(data);
        //            nodes = data.name
        //        }
        //});

        // 画出节点并保存在ops对象中{'web01':节点对象,'web02':节点对象}
        var ops = new Object();

        for (var i=0;i<nodes.length;i++){
            ops[nodes[i].hostname] = addNode(nodes[i].hostname,nodes[i].ip,nodes[i].type);
        }

        // 画出节点连线

        for (var i=0;i<links.length;i++){
            var s = links[i].source;
            var d = links[i].destination;

            var source = ops[s];
            var destination = ops[d];
            addLink(source,destination);
        }

        // 树形布局
        scene.doLayout(JTopo.layout.TreeLayout('down', 40, 120));

        // 手动绘图
        autoaddLink();

        });