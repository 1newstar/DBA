$(document).ready(function(){
            var canvas = document.getElementById('canvas');
            var stage = new JTopo.Stage(canvas);
            var scene = new JTopo.Scene(stage);
            scene.background="./img/back/03.png";
            scene.alpha = 1;

            //显示工具栏
            showJTopoToobar(stage);

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

            function addLink(nodeA, nodeZ) {
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

            var client = addNode('client','xx','internat');
            var slb = addNode('slb','xx','SLB');
            var nginx01 = addNode('Nginx','xx','ECS');
            var nginx02 = addNode('Nginx','xx','ECS');
            var database = addNode('database','xx','RDS');
            var database02 = addNode('database','xx','RDS');
            var database03 = addNode('database','xx','RDS');
            var database04 = addNode('database','xx','RDS');
            var nginx03 = addNode('Nginx','xx','ECS');



            nginx01.alarm = 'Warrning';
            nginx01.alarmColor = '255,0,0';
            nginx01.alarmAlpha = 0.9;

            addLink(client,slb);
            addLink(slb,nginx01);
            addLink(slb,nginx02);
            addLink(nginx01,database);
            addLink(nginx02,database);

            // 树形布局
            scene.doLayout(JTopo.layout.TreeLayout('down', 100, 120));
            // 手动绘图
            autoaddLink();



        });