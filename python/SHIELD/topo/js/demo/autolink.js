        $(document).ready(function(){
            var canvas = document.getElementById('canvas');
            var stage = new JTopo.Stage(canvas);
            //显示工具栏
            showJTopoToobar(stage);
            var scene = new JTopo.Scene(stage);
            scene.background = './img/back/03.png';

            var msgNode = new JTopo.TextNode("双击编辑文字, 点击节点可连线(连个节点)");
            msgNode.zIndex++;
            msgNode.setBound(250, 50);
            scene.add(msgNode);

            for(var i=0; i<5; i++){
                var node = new JTopo.Node('Node_' + i);
                node.setLocation(Math.random() * 600, Math.random() * 400);
                scene.add(node);
            }


            var beginNode = null;
            var tempNodeA = new JTopo.Node('tempA');
            tempNodeA.setSize(1, 1);

            var tempNodeZ = new JTopo.Node('tempZ');
            tempNodeZ.setSize(1, 1);

            var link = new JTopo.Link(tempNodeA, tempNodeZ);

            scene.mouseup(function(e){
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
                        var l = new JTopo.Link(beginNode, endNode);
                        scene.add(l);
                        beginNode = null;
                        scene.remove(link);
                    }else{
                        beginNode = null;
                    }
                }else{
                    scene.remove(link);
                }
            });

            scene.mousedown(function(e){
                if(e.target == null || e.target === beginNode || e.target === link){
                    scene.remove(link);
                }
            });
            scene.mousemove(function(e){
                tempNodeZ.setLocation(e.x, e.y);
            });

            //var textfield = $("#jtopo_textfield");
            //scene.dbclick(function(event){
            //    if(event.target == null) return;
            //    var e = event.target;
            //    textfield.css({
            //        top: event.pageY,
            //        left: event.pageX - e.width/2
            //    }).show().attr('value', e.text).focus().select();
            //    e.text = "";
            //    textfield[0].JTopoNode = e;
            //});

            //$("#jtopo_textfield").blur(function(){
                //textfield[0].JTopoNode.text = textfield.hide().val();
            //});

        });