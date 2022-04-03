# DMZJ_Crawler 动漫之家爬虫
<b style='color:red'>2022-04-03：该项目创建于2019年年底，目前有些接口可能早已失效</b>
<p>每隔两小时爬取一次最新的漫画信息，可爬取隐藏漫画</p>
<h2>部分接口：</h2>
<ul>
  <li><b>漫画信息</b>：http://v3api.dmzj.com/comic/comic_漫画ID.json</li>
</ul>
<table>
  <tbody>
    <tr>
      <td><b>请求方式</b></td>
      <td>GET</td>
    </tr>
    <tr><td><b>参数</b></td></tr>
    <tr>
      <td>漫画ID</td>
      <td>漫画ID</td>
      <td>可在对应的漫画专题页的控制台里通过g_comic_id查看</td>
    </tr>
    <tr><td><b>比较有用的返回值</b></td></tr>
    <tr>
      <td>title</td>
      <td>漫画名</td>
    </tr>
    <tr>
      <td>cover</td>
      <td>封面链接</td>
    </tr>
    <tr>
      <td>comic_py</td>
      <td>名称拼音</td>
      <td>可根据该拼音进入相应的专题页https://manhua.dmzj.com/+拼音</td>
    </tr>
    <tr>
      <td>hidden</td>
      <td>是否隐藏</td>
      <td>隐藏漫无法在手机端搜索到</td>
    </tr>
    <tr>
      <td>is_lock</td>
      <td>是否被锁</td>
      <td>目前可知被锁漫画为真正无法观看的漫画</td>
    </tr>
    <tr>
      <td>types</td>
      <td>漫画类型</td>
    </tr>
    <tr>
      <td>status</td>
      <td>连载状态</td>
    </tr>
    <tr>
      <td>authors</td>
      <td>作者名称</td>
      <td>是个数组</td>
    </tr>
    <tr>
      <td>chapters</td>
      <td>章节系列分支，以及每一话的信息</td>
      <td>可查看每一话的ID，名称，上传时间，文件大小</td>
    </tr>
  </tbody>
</table>

<ul>
  <li><b>获取评论</b>：https://comment.dmzj.com/v1/4/latest/漫画ID</li>
</ul>
<p>注：每页只显示40条评论</p>
<table>
  <tbody>
    <tr>
      <td><b>请求方式</b></td>
      <td>GET</td>
    </tr>
    <tr><td><b>参数</b></td></tr>
    <tr>
      <td>漫画ID</td>
      <td>漫画ID</td>
    </tr>
    <tr>
      <td>page_index</td>
      <td>该漫画的第N页评论</td>
    </tr>
    <tr><td><b>返回值</b></td></tr>
    <tr>
      <td>commentIds</td>
      <td>各评论的ID</td>
      <td>若是回复，ID用逗号隔开，第一个为当前评论ID，其余均为被回复的评论ID </td>
    </tr>
    <tr>
      <td>comments</td>
      <td>每一条评论的详细信息</td>
    </tr>
    <tr>
      <td>total</td>
      <td>该漫画的总评论数</td>
    </tr>
  </tbody>
</table>
<ul>
  <li><b>评论漫画</b>：https://comment.dmzj.com/v1/4/add/web?callback=add_sucess</li>
</ul>
<table>
  <tbody>
    <tr>
      <td><b>请求方式</b></td>
      <td>GET</td>
    </tr>
    <tr><td><b>参数</b></td></tr>
    <tr>
      <td>obj_id</td>
      <td>漫画ID</td>
    </tr>
    <tr>
      <td>sender_uid</td>
      <td>发送人ID</td>
    </tr>
    <tr>
      <td>content</td>
      <td>评论内容</td>
    </tr>
    <tr>
      <td>to_uid</td>
      <td>回复的用户ID</td>
      <td>默认为0</td>
    </tr>
    <tr>
      <td>to_comment_id</td>
      <td>回复的评论ID</td>
      <td>默认为0</td>
    </tr>
    <tr>
      <td>sender_terminal</td>
      <td>使用默认值1</td>
    </tr>
    <tr><td><b>返回值</b></td></tr>
    <tr>
      <td>code</td>
      <td>评论状态</td>
    </tr>
    <tr>
      <td>msg</td>
      <td>状态信息</td>
    </tr>
    <tr>
      <td>data</td>
      <td>该评论ID</td>
    </tr>
  </tbody>
</table>
